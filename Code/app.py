from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from schema import db, User, Influencer, Campaign, Contract, Sponsor
from dotenv import dotenv_values
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta, datetime

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

    if db.session.execute(db.select(User)).scalars().all() == []:
        admin = User(
            first_name = 'Kaiwalya',
            last_name = 'Deshpande',
            email = "kd@gmail.com",
            password = generate_password_hash(env['PASSWORD'], 'pbkdf2:sha256', 8),
            type = 0
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    user = db.session.execute(db.select(User).where(User.email == request.json['email'])).scalar()
    if user and check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(identity=request.json['email'], expires_delta=timedelta(days=30))
        return jsonify(access_token = access_token), 200
    else:
        return jsonify(message = "Incorrect ID or Password"), 401
    
@app.route('/register', methods=['POST'])
def register():
    user = db.session.execute(db.select(User).where(User.email == request.json[0]['email'])).scalar()
    if user:
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
    if user.type == 2:
        sponsor = Sponsor(
            company=request.json[1]['company'],
            industry=request.json[1]['industry'],
            budget=request.json[1]['budget'],
            user_id = user.id,
        )
        db.session.add(sponsor)
        
    elif user.type == 1:
        influencer = Influencer(
            user_id = user.id,
            platform=request.json[1]['platform'],
            reach = request.json[1]['reach'],
            niche=request.json[1]['niche']
        )
        db.session.add(influencer)
        
    db.session.commit()

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(days=30))
    return jsonify(access_token = access_token), 201
    
@app.route('/get-user-data')
@jwt_required()
def get_user_data():
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()

    return jsonify(user.serialize), 200

@app.route('/get-all-users')
@jwt_required()
def get_all_users():
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type != 0:
        return jsonify(message = "You do not have permissions to get all users"), 403
    
    all_users = db.session.execute(db.select(User)).scalars()
    return jsonify([user.serialize for user in all_users]), 200

@app.route("/campaigns", methods=['GET', 'POST'])
@jwt_required()
def get_all_campaigns():
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0: # Admin
        if request.method == 'GET': # Return all the Campaings
            campaigns = db.session.execute(db.select(Campaign)).scalars()
            return jsonify(campaigns = [campaign.serialize for campaign in campaigns]), 200
        
        # If campaign is approved changes the flagged status, else approves it
        campaign = db.session.execute(db.select(Campaign).where(Campaign.id == request.json['id'])).scalar()
        if campaign.approved:
            campaign.flagged = not campaign.flagged
            db.session.commit()
            return jsonify(message = f"The campaign flag has been set to {campaign.flagged}!"), 200
        else:
            campaign.approved = True
            db.session.commit()
            return jsonify(message = "The campaign has been approved!"), 200
    
    elif user.type == 1: # Influencer
        if request.method == 'GET': # Get the campaigns in the public and approved and not flagged
            campaigns = db.session.execute(db.select(Campaign)
                                           .where(Campaign.approved)
                                           .where(Campaign.public)
                                           .where(Campaign.flagged == False)
                                           ).scalars()
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
            return jsonify(campaigns = [campaign.serialize for campaign in user.sponsor.campaign]), 200
        
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

        return jsonify(message = "The Campaign has been created!"), 201

@app.route("/contract", methods=['GET', 'POST', 'PUT'])
@jwt_required()
def contract():
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0: # Admin
        if request.method == 'GET': # Get all current Contracts
            contracts = db.session.execute(db.select(Contract)).scalars()
            return jsonify(contracts = [contract.serialize for contract in contracts]), 200
        
        else:
            return jsonify(message="Please don't make an Ad request"), 401
    
    elif user.type == 1: # Influencer
        if request.method == 'GET': # Get all contracts that they have
            contracts = db.session.execute(db.select(Contract)
                                           .where(Contract.influencer_id == user.influencer.id)).scalars()
            return jsonify(contracts = [contract.serialize for contract in contracts]), 200
        
        elif request.method == 'PUT': # Approve or reject a pending contract
            contract = db.session.execute(db.select(Contract)
                                          .where(Contract.id == request.json['contract_id'])).scalar()
            
            if contract.status != 2:
                return jsonify(message = "The status doesn't seem to need your approval!"), 401

            contract.status = 3 if request.json['approved'] == True else 0
            db.session.commit()
            return jsonify(message="The contract action has been completed!"), 200
        
        else:
            return jsonify(message="You don't have any use of this api"), 403
    
    else: # Sponsor
        if request.method == "GET": # Get all contracts of the sponsor
            contracts = db.session.execute(db.select(Contract)
                                           .where(Contract.campaign.has(sponsor_id=user.sponsor.id))).scalars()
            return jsonify(contracts = [contract.serialize for contract in contracts]), 200
        
        elif request.method == "POST": # Create a new Campaign
            campaign = db.session.execute(db.select(Campaign)
                                          .where(Campaign.id == request.json['campaign_id'])).scalar()
            influencer = db.session.execute(db.select(Influencer)
                                            .where(Influencer.id == request.json['influencer_id'])).scalar()
            contract = Contract(
                influencer_id = influencer.id,
                campaign_id = campaign.id,
                requirements = request.json['requirements'],
                payment_amount = request.json['payment_amount'],
                status = 2 # made by sponsor
            )
            db.session.add(contract)
            db.session.commit()
            return jsonify(message="The Ad request has been sent!"), 201
        
        else: # Approve or reject the Contract
            contract = db.session.execute(db.select(Contract)
                                          .where(Contract.id == request.json['contract_id'])).scalar()
            if contract.status != 1:
                return jsonify(message = "The status doesn't seem to need your approval!"), 401
            
            contract.status = 3 if request.json['approved'] == True else 0
            db.session.commit()
            return jsonify(message="The contract action has been completed!"), 200
    
if __name__ == '__main__':

    app.run(debug=True)
    
