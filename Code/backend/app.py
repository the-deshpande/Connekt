from flask import Flask

from database.sample_data import init_db
from database.schema import db, User

from flask_cors import CORS
from flask_jwt_extended import JWTManager

from api.authentication import auth_bp
from api.users import users_bp
from api.campaigns import camp_bp
from api.contracts import cont_bp

from dotenv import dotenv_values
env = dotenv_values()

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(camp_bp, url_prefix='/campaigns')
app.register_blueprint(cont_bp, url_prefix='/contracts')

app.config['SECRET_KEY'] = env.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = env.get('JWT_SECRET_KEY')
app.config.from_object(__name__)

CORS(app, resources={r'/*':{'origins':'*'}})

jwt = JWTManager(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
with app.app_context():
    db.create_all()
    if db.session.execute(db.select(User)).scalars().all() == []:
        init_db(env['PASSWORD'])

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
