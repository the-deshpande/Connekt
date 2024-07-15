from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    influencer = db.relationship('Influencer', backref='user', uselist=False) 
    sponsor = db.relationship('Sponsor', backref='user', uselist=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    type = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "email" : self.email,
            "type" : self.type
        }

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contract = db.relationship('Contract', backref='influencer')
    platform = db.Column(db.String(250), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    niche = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "platform": self.platform,
            "reach": self.reach,
            "niche": self.niche
        }

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    campaign = db.relationship('Campaign', backref='sponsor')
    company = db.Column(db.String(250), nullable=False)
    industry = db.Column(db.String(250), nullable=False)
    budget = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "company": self.company,
            "industry": self.industry,
            "budget": self.budget
        }

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'), nullable=False)
    contract = db.relationship('Contract', backref='campaign')
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.strftime("%d-%m-%Y"),
            "end_date": self.end_date.strftime("%d-%m-%y"),
            "public": self.public,
            "goals": self.goals,
            "approved": self.approved
        }

class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    requirements = db.Column(db.String(250), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "requirements": self.requirements,
            "payment_amount": self.payment_amount,
            "status": self.status
        }
    