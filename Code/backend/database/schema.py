from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    influencer = db.relationship('Influencer', 
                                 backref=db.backref('user', cascade="all, delete", uselist=False), 
                                 cascade="all, delete", uselist=False) 
    sponsor = db.relationship('Sponsor', 
                              backref=db.backref('user', cascade="all, delete", uselist=False), 
                              cascade="all, delete", uselist=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    type = db.Column(db.Integer, nullable=False) # 0 = admin | 1 = influencer | 2 = sponsor

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "email" : self.email,
            "flagged": self.flagged,
            "type" : self.type,
            "influencer": self.influencer.serialize if self.influencer is not None else None,
            "sponsor": self.sponsor.serialize if self.sponsor is not None else None,
        }
        

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(250), nullable=False) # Youtube | TikTok | Instagram | Twitter
    reach = db.Column(db.Integer, nullable=False)
    niche = db.Column(db.String(250), nullable=False) # Healthcare | Gaming | Tech | Vlog

    @property
    def serialize(self):
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
    company = db.Column(db.String(250), nullable=False)
    industry = db.Column(db.String(250), nullable=False) # Healthcare | Gaming | Tech | Vlog
    budget = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
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
    sponsor = db.relationship('Sponsor', 
                              backref=db.backref('campaigns', cascade="all, delete", uselist=True), 
                              uselist=False)
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
            "sponsor": self.sponsor.user.serialize,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "public": self.public,
            "goals": self.goals,
            "approved": self.approved,
            "flagged": self.flagged,
        }

class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    campaign = db.relationship('Campaign', 
                               backref=db.backref('contracts', cascade="all, delete", uselist=True), 
                               uselist=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    influencer = db.relationship('Influencer', 
                                 backref=db.backref('contracts', cascade="all, delete", uselist=True), 
                                 uselist=False)
    requirements = db.Column(db.String(250), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0) # 0 = rejected | 1 = influencer | 2 = sponsor | 3 = approved

    @property
    def serialize(self):
        """ Returns dictionary that is easily serializable """
        return {
            "id": self.id,
            "campaign": self.campaign.serialize,
            "influencer": self.influencer.user.serialize,
            "requirements": self.requirements,
            "payment_amount": self.payment_amount,
            "status": self.status
        }
    