from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from database.schema import db, User, Sponsor, Influencer
from datetime import timedelta

auth_bp = Blueprint('authentication', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logs the user in
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
    
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user
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