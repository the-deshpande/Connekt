from flask import Flask, render_template, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap5
from schema import db, Users
from dotenv import dotenv_values

env = dotenv_values()

app = Flask(__name__)
app.config['SECRET_KEY'] = env.get('SECRET_KEY')
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

    # db.session.add(Users(
    #     first_name = 'Kaiwalya',
    #     last_name = 'Deshpande',
    #     username = 'the_deshpande',
    #     email = 'kaiwalya@email.com',
    #     password = generate_password_hash('ABCDEFGHIJ', 'pbkdf2:sha256', 8),
    #     type = 0
    # ))
    # db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.execute(db.select(Users).where(Users.username == request.json['username'])).scalar()
        
        if user and check_password_hash(user.password, request.json['password']):
            if login_user(user):
                return jsonify(True)
            return jsonify(False)
        else:
            return jsonify(False)

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(True)

@app.route('/loggedin')
def admin():
    if current_user:
        return jsonify(current_user.is_authenticated)
    return jsonify(True)


if __name__ == '__main__':
    app.run(debug=True)
