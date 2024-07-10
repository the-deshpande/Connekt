from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from schema import db, User, Influencer, Campaign, Contract, Sponsor
from dotenv import dotenv_values
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta

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


@app.route("/ping")
def greeting():
    return jsonify('pong')

@app.route('/login', methods=['POST'])
def login():
    user = db.session.execute(db.select(User).where(User.email == request.json['email'])).scalar()
    if user and check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(identity=request.json['email'], expires_delta=timedelta(days=1))
        return jsonify(access_token = access_token), 200
    else:
        return jsonify(message = "Incorrect ID or Password"), 401
    
@app.route('/register', methods=['POST'])
def register():
    user = db.session.execute(db.select(User).where(User.email == request.json[0]['email'])).scalar()
    if user:
        return jsonify(message = 'User with this Email already exists!'), 401
    
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

    if request.json[0]['type'] == "2":
        sponsor = Sponsor(
            company=request.json[1]['company'],
            industry=request.json[1]['industry'],
            budget=request.json[1]['budget'],
            user_id = user.id,
        )
        db.session.add(sponsor)
        
    elif request.json[0]['type'] == "1":
        influencer = Influencer(
            user_id = user.id,
            platform=request.json[1]['platform'],
            reach = request.json[1]['reach'],
            niche=request.json[1]['niche']
        )
        db.session.add(influencer)
        
    db.session.commit()

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
    return jsonify(access_token = access_token), 200
    
@app.route('/get-user-data')
@jwt_required()
def get_user_data():
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()

    return jsonify({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'type': user.type,
    }), 200

@app.route('/get-all-users')
@jwt_required()
def get_all_users():
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if(user.type != 0):
        return jsonify(message = "You do not have permissions for this"), 401
    
    all_users = db.session.execute(db.select(User)).scalars()
    all_users_dict = []
    for users in all_users:
        all_users_dict.append({
        'first_name': users.first_name,
        'last_name': users.last_name,
        'email': users.email,
        'type': users.type,
        })
    return jsonify(all_users_dict), 200


if __name__ == '__main__':
    app.run(debug=True)
