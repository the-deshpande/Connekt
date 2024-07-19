from database.schema import db, User, Influencer, Sponsor, Campaign, Contract
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_db(admin_password):
    # Admin
    admin = User(first_name = 'Kaiwalya', last_name = 'Deshpande', email = "kd@gmail.com", password = generate_password_hash(admin_password, 'pbkdf2:sha256', 8), type = 0)
    db.session.add(admin)
    db.session.commit()

    # 5 Influencers
    for i in range(5):
        user = User(first_name = 'Influencer', last_name = f'{i}', email = f"influencer{i}@gmail.com", password = generate_password_hash("1234", 'pbkdf2:sha256', 8), type = 1)
        db.session.add(user)
        db.session.commit()

        user = db.session.execute(db.select(User).where(User.email == user.email)).scalar()
        inf = Influencer(user_id = user.id, platform="Youtube", reach=i*100, niche="Gaming")
        db.session.add(inf)
        db.session.commit()

    # 5 Sponsor
    for i in range(5):
        user = User(first_name = 'Sponsor', last_name = f'{i}', email = f"sponsor{i}@gmail.com", password = generate_password_hash("1234", 'pbkdf2:sha256', 8), type = 2)
        db.session.add(user)
        db.session.commit()

        user = db.session.execute(db.select(User).where(User.email == user.email)).scalar()
        spo = Sponsor(user_id = user.id, company="Sponsor Co.", budget=i*100, industry="Gaming")
        db.session.add(spo)
        db.session.commit()
    
    # 2 campaigns for each Sponsor 1 public and 1 private
    # 5 contracts from campaign to influencer
    sponsors = db.session.execute(db.select(User).where(User.type == 2)).scalars()
    for sponsor in sponsors:
        camp1 = Campaign(sponsor_id=sponsor.sponsor.id, name=f"Campaign {sponsor.sponsor.id}", description="This is a public Campaign",
                         start_date=datetime.strptime('01-01-2024',"%d-%m-%Y"), end_date=datetime.strptime('31-12-2024',"%d-%m-%Y"), public=True, goals=sponsor.sponsor.id * 1000)
        camp2 = Campaign(sponsor_id=sponsor.sponsor.id, name=f"Campaign {sponsor.sponsor.id}", description="This is a private Campaign",
                         start_date=datetime.strptime('01-01-2024',"%d-%m-%Y"), end_date=datetime.strptime('31-12-2024',"%d-%m-%Y"), public=False, goals=sponsor.sponsor.id * 1000)
        db.session.add(camp1)
        db.session.add(camp2)
        db.session.commit()

    infs = db.session.execute(db.select(User).where(User.type == 1)).scalars().all()
    camps = db.session.execute(db.select(Campaign).where(Campaign.public == False)).scalars().all()
    for i in range(5):
        contract = Contract(influencer_id=infs[i].influencer.id, campaign_id=camps[i].id,
                            requirements="Just saying Hello", status=2, payment_amount=1000)
        db.session.add(contract)
        db.session.commit()
    
    camps = db.session.execute(db.select(Campaign).where(Campaign.public)).scalars().all()
    for i in range(5):
        contract = Contract(influencer_id=infs[i].influencer.id, campaign_id=camps[i].id,
                            requirements="Replying to Hello", status=1, payment_amount=1000)
        db.session.add(contract)
        db.session.commit()
        
