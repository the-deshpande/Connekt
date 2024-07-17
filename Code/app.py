from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from schema import db, User, Influencer, Campaign, Contract, Sponsor
from dotenv import dotenv_values
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta, datetime
from database import add_starter_data

env = dotenv_values()

app = Flask(__name__)
app.config['SECRET_KEY'] = env.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = env.get('JWT_SECRET_KEY')
app.config.from_object(__name__)

CORS(app, resources={r'/*':{'origins':'*'}})

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

with app.app_context():
    db.create_all()

    # Create sample data
    if db.session.execute(db.select(User)).scalars().all() == []:
        add_starter_data(env['PASSWORD'])

@app.route('/login', methods=['POST'])
def login():
    """
    POST: Logs the user in

    JSON input: {
        "email": #Value,
        "password:: #Value,
    }
    """
    user = db.session.execute(db.select(User).where(User.email == request.json['email'])).scalar()
    if user and check_password_hash(user.password, request.json['password']):
        # if the user is flagged by admin, prevent login
        if user.flagged == True:
            return jsonify(message = "The user is flagged"), 403
        access_token = create_access_token(identity=request.json['email'], expires_delta=timedelta(days=30))
        return jsonify(access_token = access_token, user=user.serialize), 200
    else:
        return jsonify(message = "Incorrect ID or Password"), 401
    
@app.route('/register', methods=['POST'])
def register():
    """
    POST: Registers a new user

    JSON input: [
        {
            "first_name": #Value,
            "last_name": #Value,
            "email": #Value,
            "password": #Value,
            "type": #Value,
        },
        # If sponsor
        {
            "company": #Value,
            "industry": #Value,
            "budget": #Value,
        }
        # If influencer
        {
            "platform": #Value,
            "reach": #Value,
            "niche": #Value,
        }
    ]
    """
    user = db.session.execute(db.select(User).where(User.email == request.json[0]['email'])).scalar()
    if user: # only one account per email 
        return jsonify(message = 'User with this Email already exists!'), 409
    
    user = User(
        first_name = request.json[0]['first_name'],
        last_name = request.json[0]['last_name'],
        email = request.json[0]['email'],
        password = generate_password_hash(request.json[0]['password'], 'pbkdf2:sha256', 8),
        type = request.json[0]['type']
    )
    db.session.add(user)
    db.session.commit()

    user = db.session.execute(db.select(User).where(User.email == request.json[0]['email'])).scalar()
    if user.type == 2: # Sponsor
        sponsor = Sponsor(
            company=request.json[1]['company'],
            industry=request.json[1]['industry'],
            budget=request.json[1]['budget'],
            user_id = user.id,
        )
        db.session.add(sponsor)
        
    elif user.type == 1: # Influencer
        influencer = Influencer(
            user_id = user.id,
            platform=request.json[1]['platform'],
            reach = request.json[1]['reach'],
            niche=request.json[1]['niche']
        )
        db.session.add(influencer)
        
    db.session.commit()

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(days=30))
    return jsonify(access_token = access_token, user = user.serialize), 201
    
@app.route('/get-user-data', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def get_user_data():
    """
    GET: Returns the current users data
    PUT: Updates the current users data
    DELETE: Deletes the current user
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if request.method == 'GET':
        return jsonify(user.serialize), 200
    
    elif request.method == 'DELETE':
        if user.type == 0:
            return jsonify(message="Admin account cannot be deleted"), 401
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="The user has been deleted successfully"), 200
    
    user.first_name = request.json['first_name']
    user.last_name = request.json['last_name']
    if user.sponsor:
        user.sponsor.industry = request.json['sponsor']['industry']
        user.sponsor.company = request.json['sponsor']['company']
        user.sponsor.budget = request.json['sponsor']['budget']
    if user.influencer:
        user.influencer.platform = request.json['influencer']['platform']
        user.influencer.niche = request.json['influencer']['niche']
        user.influencer.reach = request.json['influencer']['reach']
    db.session.commit()
    return jsonify(message = "The user data has been updated"), 200


@app.route('/all-users', methods=['GET', 'POST'])
@jwt_required()
def all_users():
    """
    GET:{
        Admin: returns all the users data
        Sponsor: returns all the non flagged influencers
    }

    POST: Updates the user flag status

    JSON input:{
        "user_id": #Value,
    }
    """
    curr_user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    
    if request.method == 'GET': # Return list of all users
        if curr_user.type == 0:
            all_users = db.session.execute(db.select(User)).scalars()
            return jsonify(users = [user.serialize for user in all_users]), 200
        elif curr_user.type == 2:
            all_users = db.session.execute(db.select(User)
                                           .where(User.flagged == False)
                                           .where(User.type == 1)).scalars()
            return jsonify(users = [user.serialize for user in all_users]), 200
        else:
            return jsonify(message="You do not have permissions to view this"), 403
            
    
    # Flag or unflag a user
    if curr_user.type != 0:
        return jsonify(message = "You do not have permissions to make this request"), 403

    user = db.session.execute(db.select(User).where(User.id == request.json['user_id'])).scalar()
    user.flagged = not user.flagged
    return jsonify(message="The user flag has been updated"), 200

@app.route("/campaigns", methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def campaigns():
    """
    GET: {
        Admin: Returns all the campaigns
        Sponsor: Returns all the campaigns of the sponsor
        Influencer: Returns all the public campaigns that are not flagged
    }

    POST: {
        Admin: If the campaign is not approved then approves it or else updates the flag status
        Sponsor: Creates a new campaign
        Influencer: Creates an ad request for a selected Campaign
    }
    
    PUT: {
        Admin: Updates a selected campaign
        Sponsor: Updates a selected campaign
    }

    DELETE: {
        Admin: Deletes a selected campaign and the contracts related to it
        Sponsor: Deletes a selected campaign and the contracts related to it
    }
    
    JSON input:
    Admin POST: {
        "campaign_id": #Value,
    }
    Admin PUT: {
        "campaign_id": #Value,
        "name": #Value,
        "desc": #Value,
        "start": #Value,
        "end": #Value,
        "public": #Value,
        "goals": #Value,
    }
    Admin DELETE: {
        "campaign_id": #Value,
    }
    Sponsor POST: {
        "name": #Value,
        "desc": #Value,
        "start": #Value,
        "end": #Value,
        "public": #Value,
        "goals": #Value,
    }
    Sponsor PUT: {
        "campaign_id": #Value,
        "name": #Value,
        "desc": #Value,
        "start": #Value,
        "end": #Value,
        "public": #Value,
        "goals": #Value,
    }
    Sponsor DELETE: {
        "campaign_id": #Value,
    }
    Influencer: {
        "campaign_id": #Value,
        "requirements": #Value,
        "payment_amount": #Value,
    }
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0: # Admin
        if request.method == 'GET': # Return all the Campaings
            campaigns = db.session.execute(db.select(Campaign)).scalars()
            return jsonify(campaigns = [campaign.serialize for campaign in campaigns]), 200
        
        if request.method == 'PUT':
            campaign = db.session.execute(db.select(Campaign)
                                          .where(Campaign.id == request.json['campaign_id'])).scalar()
            if campaign is None:
                return jsonify(message="Incorrect Campaign ID"), 404
            
            campaign.name = request.json['name']
            campaign.description = request.json['desc']
            campaign.start_date = datetime.strptime(request.json['start'], '%d-%m-%Y').date()
            campaign.end_date = datetime.strptime(request.json['end'], '%d-%m-%Y').date()
            campaign.public = request.json['public'] == 'true'
            campaign.goals = int(request.json['goals'])

            db.session.commit()
            return jsonify(message = "The campaign has been updated!"), 200
        
        if request.method == 'DELETE':
            campaign = db.session.execute(db.select(Campaign)
                                          .where(Campaign.id == request.json['campaign_id'])).scalar()
            if campaign is None:
                return jsonify(message="Incorrect Campaign ID"), 404
            
            db.session.delete(campaign)
            db.session.commit()
            return jsonify(message="The campaign has been successfully deleted"), 202

        # If campaign is approved changes the flagged status, else approves it
        campaign = db.session.execute(db.select(Campaign).where(Campaign.id == request.json['campaign_id'])).scalar()
        if campaign.approved:
            campaign.flagged = not campaign.flagged
            db.session.commit()
            return jsonify(message = "The campaign flag status has been updated!"), 200
        else:
            campaign.approved = True
            db.session.commit()
            return jsonify(message = "The campaign has been approved!"), 200
    
    elif user.type == 1: # Influencer
        if request.method == 'GET': # Get the campaigns in the public and approved and not flagged
            campaigns = db.session.execute(db.select(Campaign).where(Campaign.approved)
                                           .where(Campaign.public).where(Campaign.flagged == False)).scalars()
            return jsonify(campaigns = [campaign.serialize for campaign in campaigns]), 200
        
        campaign = db.session.execute(db.select(Campaign).where(Campaign.id == request.json['campaign_id'])).scalar()
        contract = Contract(
            influencer_id = user.influencer.id,
            campaign_id = campaign.id,
            requirements = request.json['requirements'],
            payment_amount = request.json['payment_amount'],
            status = 1 # made by influencer
        )
        db.session.add(contract)
        db.session.commit()

        return jsonify(message = "The Ad request has been sent!"), 201
        
    else: # Sponsor
        if request.method == 'GET': # Get all your campaings
            return jsonify(campaigns = [campaign.serialize for campaign in user.sponsor.campaigns]), 200
        
        if request.method == 'PUT': # Update a campaign
            campaign = db.session.execute(db.select(Campaign)
                                          .where(Campaign.id == request.json['campaign_id'])
                                          .where(Campaign.sponsor_id == user.sponsor.id)).scalar()
            if campaign is None:
                return jsonify(message="Incorrect Campaign ID"), 401
            
            campaign.name = request.json['name']
            campaign.description = request.json['desc']
            campaign.start_date = datetime.strptime(request.json['start'], '%d-%m-%Y').date()
            campaign.end_date = datetime.strptime(request.json['end'], '%d-%m-%Y').date()
            campaign.public = request.json['public'] == 'true'
            campaign.goals = int(request.json['goals'])
            campaign.approved = False

            db.session.commit()
            return jsonify(message = "The campaign has been updated and the changes are put up for approval!"), 200
        
        if request.method == 'DELETE': # Delete a campaign
            campaign = db.session.execute(db.select(Campaign)
                                          .where(Campaign.id == request.json['campaign_id'])
                                          .where(Campaign.sponsor_id == user.sponsor.id)).scalar()
            if campaign is None:
                return jsonify(message="Incorrect Campaign ID"), 401
            
            db.session.delete(campaign)
            db.session.commit()
            return jsonify(message="The campaign has been successfully deleted"), 202
        
        # Create a new campaign
        campaign = Campaign(
            sponsor_id = user.sponsor.id,
            name = request.json['name'],
            description = request.json['desc'],
            start_date = datetime.strptime(request.json['start'], '%d-%m-%Y').date(),
            end_date = datetime.strptime(request.json['end'], '%d-%m-%Y').date(),
            public = request.json['public'] == 'true',
            goals = int(request.json['goals']),
        )

        db.session.add(campaign)
        db.session.commit()

        return jsonify(message = "The Campaign has been created and put up for approval!"), 201

@app.route("/contract", methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def contract():
    """
    GET: {
        Admin: Gets all the contracts
        Influencer: Gets all the contracts they are a part of
        Sponsor: Gets all the contracts they are a part of
    }

    POST: {
        Sponsor: Creates a new contract
    }

    PUT: {
        Admin: Updates the contract but cannot approve or reject it
        Influencer: Approves or rejects a contract or edits it if the request is from sponsor
        Sponsor: Approves or rejects a contract or edits it if the request is from influencer
    }

    DELETE: {
        Admin: Deletes any contract
        Influencer: Deletes the contract they are part of
        Sponsor: Deletes the contract they are part of
    }

    JSON input:
    Admin PUT: {
        "contract_id": #Value,
        "requirements": #Value,
        "payment_amount": #Value,
    }
    Admin DELETE: {
        "contract_id": #Value,
    }
    Sponsor POST: {
        "campaign_id": #Value,
        "influencer_id": #Value,
        "requirements": #Value,
        "payment_amount": #Value
    }
    Sponsor PUT: {
        "contract_id": #Value,
        "requirements": #Value,
        "payment_amount": #Value,
        "status": #Value,
    }
    Sponsor DELETE: {
        "contract_id": #Value,
    }
    Influencer PUT: {
        "contract_id": #Value,
        "requirements": #Value,
        "payment_amount": #Value,
        "status": #Value,
    }
    Influencer DELETE: {
        "contract_id": #Value,
    }
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0: # Admin
        if request.method == 'GET': # Get all current Contracts
            contracts = db.session.execute(db.select(Contract)).scalars()
            return jsonify(contracts = [contract.serialize for contract in contracts]), 200
        
        if request.method == 'PUT': # Edit a contract
            contract = db.session.execute(db.select(Contract).where(Contract.id == request.json['contract_id'])).scalar()
            
            if contract is None:
                return jsonify(message="Some problem occured while retrieving contract"), 401
            
            if contract.status in [0, 3]:
                return jsonify(message="The contract has already been processed!"), 401
            
            contract.requirements = request.json['requirements']
            contract.payment_amount = request.json['payment_amount']
            db.session.commit()
            return jsonify(message="The contract has been updated"), 200
        
        if request.method == 'DELETE': # Delete a contract
            contract = db.session.execute(db.select(Contract).where(Contract.id == request.json['contract_id'])).scalar()
            
            if contract is None:
                return jsonify(message="Some problem occured while retrieving contract"), 401

            db.session.delete(contract)
            db.session.commit()
            return jsonify(message="The contract has been successfully deleted"), 202
        
        else:
            return jsonify(message="Please don't make an Ad request"), 401
    
    elif user.type == 1: # Influencer
        if request.method == 'GET': # Get all contracts that they have
            contracts = db.session.execute(db.select(Contract)
                                           .where(Contract.influencer_id == user.influencer.id)).scalars()
            return jsonify(contracts = [contract.serialize for contract in contracts]), 200
        
        if request.method == 'PUT': # Approve or reject a pending contract
            contract = db.session.execute(db.select(Contract)
                                          .where(Contract.id == request.json['contract_id'])
                                          .where(Contract.influencer_id == user.influencer.id)).scalar()
            
            if contract is None:
                return jsonify(message="Some problem occured while retrieving contract"), 401
            
            if contract.status != 2:
                return jsonify(message = "The status doesn't seem to need your approval!"), 401
            
            if request.json['status'] != 2:
                contract.status = request.json['status']
                db.session.commit()
                return jsonify(message="The contract action has been completed!"), 200
            
            contract.requirements = request.json['requirements']
            contract.payment_amount = request.json['payment_amount']
            contract.status = 1 # Sent by influencer
            db.session.commit()
            return jsonify(message="The contract has been updated"), 200
        
        if request.method == 'DELETE': # Delete a contract
            contract = db.session.execute(db.select(Contract)
                                          .where(Contract.id == request.json['contract_id'])
                                          .where(Contract.influencer_id == user.influencer.id)).scalar()
            
            if contract is None:
                return jsonify(message="Some problem occured while retrieving contract"), 401

            db.session.delete(contract)
            db.session.commit()
            return jsonify(message="The contract has been successfully deleted"), 202

        else:
            return jsonify(message="You don't have any use of this api"), 403
    
    else: # Sponsor
        if request.method == "GET": # Get all contracts of the sponsor
            contracts = db.session.execute(db.select(Contract)
                                           .where(Contract.campaign.has(sponsor_id=user.sponsor.id))).scalars()
            return jsonify(contracts = [contract.serialize for contract in contracts]), 200
        
        if request.method == "POST": # Create a new Contract
            campaign = db.session.execute(db.select(Campaign)
                                          .where(Campaign.id == request.json['campaign_id'])
                                          .where(Campaign.approved).where(Campaign.flagged == False)
                                          .where(Contract.campaign.has(sponsor_id=user.sponsor.id))).scalar()
            influencer = db.session.execute(db.select(User)
                                            .where()
                                            .where(User.influencer.has(id = request.json['influencer_id']))).scalar()
            
            if campaign is None or influencer is None:
                return jsonify(message="Some error occured while quering the campaign and influencer"), 404
            contract = Contract(
                influencer_id = user.influencer.id,
                campaign_id = campaign.id,
                requirements = request.json['requirements'],
                payment_amount = request.json['payment_amount'],
                status = 2 # made by sponsor
            )
            db.session.add(contract)
            db.session.commit()
            return jsonify(message="The Ad request has been sent!"), 201
        
        if request.method == "PUT": # Edit the contract or approve it
            contract = db.session.execute(db.select(Contract)
                                          .where(Contract.id == request.json['contract_id'])
                                          .where(Contract.campaign.has(sponsor_id = user.sponsor.id))).scalar()
            if contract is None:
                return jsonify(message="Some problem occured while retrieving contract"), 401

            if contract.status != 1:
                return jsonify(message = "The status doesn't seem to need your approval!"), 401
            
            if request.json['status'] != 2:
                contract.status = request['status']
                db.session.commit()
                return jsonify(message="The contract action has been completed!"), 200
            
            contract.requirements = request.json['requirements']
            contract.payment_amount = request.json['payment_amount']
            contract.status = 2 # Sent by sponsor
            db.session.commit()
            return jsonify(message="The contract has been updated"), 200
    
        # Delete a contract
        contract = db.session.execute(db.select(Contract)
                                        .where(Contract.id == request.json['contract_id'])
                                        .where(Contract.campaign.has(sponsor_id = user.sponsor.id))).scalar()
        
        if contract is None:
            return jsonify(message="Some problem occured while retrieving contract"), 401

        db.session.delete(contract)
        db.session.commit()
        return jsonify(message="The contract has been successfully deleted"), 202

if __name__ == '__main__':
    app.run(debug=True)
