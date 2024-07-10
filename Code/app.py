from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from schema import db, Users
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


@app.route("/ping")
def greeting():
    return jsonify('pong')

@app.route('/login', methods=['POST'])
def login():
    user = db.session.execute(db.select(Users).where(Users.email == request.json['email'])).scalar()
    if user and check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(identity=request.json['email'], expires_delta=timedelta(days=1))
        return jsonify(access_token = access_token), 200
    else:
        return jsonify(message = "Incorrect ID or Password"), 401
    
@app.route('/register', methods=['POST'])
def register():
    user = db.session.execute(db.select(Users).where(Users.email == request.json['email'])).scalar()
    if user:
        return jsonify(message = 'User with this Email already exists!'), 401
    
    user = Users(
        first_name = request.json['first_name'],
        last_name = request.json['last_name'],
        email = request.json['email'],
        password = generate_password_hash(request.json['password'], 'pbkdf2:sha256', 8),
        type = request.json['type']
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
    return jsonify(access_token = access_token), 200
    
@app.route('/get-user-data')
@jwt_required()
def loggedin():
    user = db.session.execute(db.select(Users).where(Users.email == get_jwt_identity())).scalar()

    return jsonify({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'type': user.type,
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
