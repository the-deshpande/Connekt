from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.schema import db, User, Contract, Campaign

cont_bp = Blueprint('contracts', __name__)

@cont_bp.route("/")
@jwt_required()
def contract():
    """
    Admin: Gets all the contracts
    Influencer: Gets all the contracts they are a part of
    Sponsor: Gets all the contracts they are a part of
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0: 
        contracts = db.session.execute(db.select(Contract)).scalars()
        return jsonify(contracts = [contract.serialize for contract in contracts]), 200
    
    elif user.type == 1: 
        contracts = db.session.execute(db.select(Contract)
                                        .where(Contract.influencer_id == user.influencer.id)).scalars()
        return jsonify(contracts = [contract.serialize for contract in contracts]), 200
    
    else: 
        contracts = db.session.execute(db.select(Contract)
                                        .where(Contract.campaign.has(sponsor_id=user.sponsor.id))).scalars()
        return jsonify(contracts = [contract.serialize for contract in contracts]), 200

@cont_bp.route("/create", methods=['POST'])
@jwt_required()
def create():
    """
    Creates a new Contract
    Only for Sponsors and Influencers
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        return jsonify(message="Please don't make an Ad request"), 401
    
    elif user.type == 1:
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

    else:
        campaign = db.session.execute(db.select(Campaign)
                                        .where(Campaign.id == request.json['campaign_id'])
                                        .where(Campaign.approved).where(Campaign.flagged == False)).scalar()
        influencer = db.session.execute(db.select(User)
                                        .where(User.influencer.has(id = request.json['influencer_id']))).scalar()
        if campaign is None or influencer is None:
            return jsonify(message="Some error occured while quering the campaign and influencer"), 404
        contract = Contract(
            influencer_id = influencer.influencer.id,
            campaign_id = campaign.id,
            requirements = request.json['requirements'],
            payment_amount = request.json['payment_amount'],
            status = 2 # made by sponsor
        )
        db.session.add(contract)
        db.session.commit()
        return jsonify(message="The Ad request has been sent!"), 201

@cont_bp.route("/edit", methods=['PUT'])
@jwt_required()
def edit():
    """
    Admin: Updates the contract but cannot approve or reject it
    Influencer: Approves or rejects a contract or edits it if the request is from sponsor
    Sponsor: Approves or rejects a contract or edits it if the request is from influencer
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        contract = db.session.execute(db.select(Contract).where(Contract.id == request.json['id'])).scalar()
        if contract is None:
            return jsonify(message="Some problem occured while retrieving contract"), 401
        if contract.status in [0, 3]:
            return jsonify(message="The contract has already been processed!"), 401
        
        contract.requirements = request.json['requirements']
        contract.payment_amount = request.json['payment_amount']
        db.session.commit()
        return jsonify(message="The contract has been updated"), 200
    
    elif user.type == 1:
        contract = db.session.execute(db.select(Contract)
                                        .where(Contract.id == request.json['id'])
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
    
    else:
        contract = db.session.execute(db.select(Contract)
                                        .where(Contract.id == request.json['id'])
                                        .where(Contract.campaign.has(sponsor_id = user.sponsor.id))).scalar()
        if contract is None:
            return jsonify(message="Some problem occured while retrieving contract"), 401
        if contract.status != 1:
            return jsonify(message = "The status doesn't seem to need your approval!"), 401
        
        if request.json['status'] != 1:
            contract.status = request.json['status']
            db.session.commit()
            return jsonify(message="The contract action has been completed!"), 200
        
        contract.requirements = request.json['requirements']
        contract.payment_amount = request.json['payment_amount']
        contract.status = 2 # Sent by sponsor
        db.session.commit()
        return jsonify(message="The contract has been updated"), 200

@cont_bp.route("/delete", methods=['DELETE'])
@jwt_required()
def delete():
    """
    Admin: Deletes any contract
    Influencer: Deletes the contract they are part of
    Sponsor: Deletes the contract they are part of
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        contract = db.session.execute(db.select(Contract).where(Contract.id == request.json['contract_id'])).scalar()
        if contract is None:
            return jsonify(message="Some problem occured while retrieving contract"), 401

        db.session.delete(contract)
        db.session.commit()
        return jsonify(message="The contract has been successfully deleted"), 202
    
    elif user.type == 1:
        contract = db.session.execute(db.select(Contract)
                                        .where(Contract.id == request.json['contract_id'])
                                        .where(Contract.influencer_id == user.influencer.id)).scalar()
        if contract is None:
            return jsonify(message="Some problem occured while retrieving contract"), 401

        db.session.delete(contract)
        db.session.commit()
        return jsonify(message="The contract has been successfully deleted"), 202
    
    else:
        contract = db.session.execute(db.select(Contract)
                                        .where(Contract.id == request.json['contract_id'])
                                        .where(Contract.campaign.has(sponsor_id = user.sponsor.id))).scalar()
        if contract is None:
            return jsonify(message="Some problem occured while retrieving contract"), 401

        db.session.delete(contract)
        db.session.commit()
        return jsonify(message="The contract has been successfully deleted"), 202
