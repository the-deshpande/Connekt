from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.schema import db, User, Campaign
from datetime import datetime

camp_bp = Blueprint('campaigns', __name__)

@camp_bp.route("/", methods=['GET'])
@jwt_required()
def campaigns():
    """
    Admin: Returns all the campaigns
    Sponsor: Returns all the campaigns of the sponsor
    Influencer: Returns all the public campaigns that are not flagged
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        campaigns = db.session.execute(db.select(Campaign)).scalars()
        return jsonify(campaigns = [campaign.serialize for campaign in campaigns]), 200

    elif user.type == 2:
        return jsonify(campaigns = [campaign.serialize for campaign in user.sponsor.campaigns]), 200
        
    else:
        campaigns = db.session.execute(db.select(Campaign).where(Campaign.approved)
                                        .where(Campaign.public).where(Campaign.flagged == False)).scalars()
        return jsonify(campaigns = [campaign.serialize for campaign in campaigns]), 200

@camp_bp.route("/delete", methods=['DELETE'])
@jwt_required()
def delete():
    """
    Admin: Deletes a selected campaign and the contracts related to it
    Sponsor: Deletes a selected campaign and the contracts related to it
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        campaign = db.session.execute(db.select(Campaign)
                                        .where(Campaign.id == request.json['campaign_id'])).scalar()
        if campaign is None:
            return jsonify(message="Incorrect Campaign ID"), 404
        
        db.session.delete(campaign)
        db.session.commit()
        return jsonify(message="The campaign has been successfully deleted"), 202

    elif user.type == 2:
        campaign = db.session.execute(db.select(Campaign)
                                        .where(Campaign.id == request.json['campaign_id'])
                                        .where(Campaign.sponsor_id == user.sponsor.id)).scalar()
        if campaign is None:
            return jsonify(message="Incorrect Campaign ID"), 401
        
        db.session.delete(campaign)
        db.session.commit()
        return jsonify(message="The campaign has been successfully deleted"), 202
    
    else:
        return jsonify(message="You are not authorized to use these!"), 401

@camp_bp.route("/create", methods=['POST'])
@jwt_required()
def create():
    """
    Admin: If the campaign is not approved then approves it or else updates the flag status
    Sponsor: Creates a new campaign
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()

    if user.type == 0:
        campaign = db.session.execute(db.select(Campaign).where(Campaign.id == request.json['campaign_id'])).scalar()
        if campaign.approved:
            campaign.flagged = not campaign.flagged
            db.session.commit()
            return jsonify(message = "The campaign flag status has been updated!"), 200
        else:
            campaign.approved = True
            db.session.commit()
            return jsonify(message = "The campaign has been approved!"), 200
        
    elif user.type == 2:
        campaign = Campaign(
            sponsor_id = user.sponsor.id,
            name = request.json['name'],
            description = request.json['description'],
            start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d').date(),
            end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d').date(),
            public = request.json['public'] == 'true',
            goals = int(request.json['goals']),
        )

        db.session.add(campaign)
        db.session.commit()

        return jsonify(message = "The Campaign has been created and put up for approval!"), 201
    
    else:
        return jsonify(message="You are not authorized to use these!"), 401

@camp_bp.route("/edit", methods=['PUT'])
@jwt_required()
def edit():
    """
    Updates a selected campaign
    Only for Admin and Sponsor
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        campaign = db.session.execute(db.select(Campaign)
                                        .where(Campaign.id == request.json['id'])).scalar()
        if campaign is None:
            return jsonify(message="Incorrect Campaign ID"), 404
        
        campaign.name = request.json['name']
        campaign.description = request.json['description']
        campaign.start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d').date()
        campaign.end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d').date()
        campaign.public = request.json['public']
        campaign.goals = int(request.json['goals'])

        db.session.commit()
        return jsonify(message = "The campaign has been updated!"), 200
    
    elif user.type == 2:
        campaign = db.session.execute(db.select(Campaign)
                                        .where(Campaign.id == request.json['id'])
                                        .where(Campaign.sponsor_id == user.sponsor.id)).scalar()
        if campaign is None:
            return jsonify(message="Incorrect Campaign ID"), 401
        
        campaign.name = request.json['name']
        campaign.description = request.json['description']
        campaign.start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d').date()
        campaign.end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d').date()
        campaign.public = request.json['public']
        campaign.goals = int(request.json['goals'])
        campaign.approved = False

        db.session.commit()
        return jsonify(message = "The campaign has been updated and the changes are put up for approval!"), 200
    
    else:
        return jsonify(message="You are not authorized to use these!"), 401

