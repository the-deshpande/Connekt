from flask import Flask
from tasks import make_celery
from celery.schedules import crontab

from database.sample_data import init_db
from database.schema import db, User

from flask_cors import CORS
from flask_jwt_extended import JWTManager

from api.authentication import auth_bp
from api.users import users_bp
from api.campaigns import camp_bp
from api.contracts import cont_bp
from api.tasks import tasks_bp

from dotenv import dotenv_values
env = dotenv_values()

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(camp_bp, url_prefix='/campaigns')
app.register_blueprint(cont_bp, url_prefix='/contracts')
app.register_blueprint(tasks_bp, url_prefix='/tasks')

app.config.from_prefixed_env()
app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
            beat_schedule={
                "daily-reminder":{
                    'task':"tasks.daily_reminder",
                    'schedule': crontab(minute=0, hour=9),
                    'relative': True,
                },
                'monthly-reminder':{
                    'task':'tasks.monthly_reminder',
                    'schedule': crontab(minute=0, hour=0, day_of_month=1),
                    'relative': True,
                }
            }
        ),
    )

celery = make_celery(app)

CORS(app, resources={r'/*':{'origins':'*'}})

jwt = JWTManager(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/instances/users.db'
db.init_app(app)
with app.app_context():
    db.create_all()
    if db.session.execute(db.select(User)).scalars().all() == []:
        init_db(env['PASSWORD'])

if __name__ == '__main__':
    app.run(debug=True)
