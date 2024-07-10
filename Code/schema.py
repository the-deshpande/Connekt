from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    type = db.Column(db.Integer, nullable=False)

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(250), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    niche = db.Column(db.String(250), nullable=False)

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company = db.Column(db.String(250), nullable=False)
    industry = db.Column(db.String(250), nullable=False)
    budget = db.Column(db.Integer, nullable=False)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)

class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    requirements = db.Column(db.String(250), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)
