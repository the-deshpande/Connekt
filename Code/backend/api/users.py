from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.schema import db, User

users_bp = Blueprint('Users', __name__)

@users_bp.route('/')
@jwt_required()
def user():
    """
    Returns the current users data
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    return jsonify(user.serialize), 200

@users_bp.route('/edit-user', methods=['PUT'])
@jwt_required()
def edit_user():
    """
    Updates the data of the current user
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
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

@users_bp.route("/delete-user", methods=['DELETE'])
@jwt_required()
def delete_user():
    """
    Deletes the current user
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if user.type == 0:
        return jsonify(message="Admin account cannot be deleted"), 401
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="The user has been deleted successfully"), 200

@users_bp.route('/users')
@jwt_required()
def users():
    """
    Admin: returns all the users data
    Sponsor: returns all the non flagged influencers
    """
    curr_user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
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
    
@users_bp.route('/flag', methods=['POST'])
@jwt_required()
def flag():
    """
    Flags the selected user
    Only for Admins
    """
    curr_user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if curr_user.type != 0:
        return jsonify(message = "You do not have permissions to make this request"), 403

    user = db.session.execute(db.select(User).where(User.id == request.json['user_id'])).scalar()
    if not user:
        return jsonify(message="User doesn't exist"), 404
    if user.type == 0:
        return jsonify(message="Admin can't be flagged"), 401
    user.flagged = not user.flagged
    db.session.commit()
    return jsonify(message="The user flag has been updated"), 200

@users_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    """
    Deletes the selected user
    """
    user = db.session.execute(db.select(User).where(User.id == request.json['user_id'])).scalar()
    if user.type == 0:
        return jsonify(message="Admin account cannot be deleted"), 401
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="The user has been deleted successfully"), 200
