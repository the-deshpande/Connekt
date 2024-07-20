from celery import Celery, Task, shared_task
from flask import Flask

from database.schema import db, Contract, User, Campaign

import pandas as pd
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values
env = dotenv_values()

def make_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def send_mail(attachment, message):
    if attachment:
        with open(f"./instances/{attachment}", "rb") as f:
            file = MIMEApplication(
                    f.read(),
                    Name=attachment,
                )
        message.attach(file)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=env.get('SMTP_EMAIL'), password=env.get('SMTP_PASSWORD'))
        connection.sendmail(from_addr=env.get('SMTP_EMAIL'), to_addrs=message['To'], msg=message.as_string())

@shared_task(ignore_result=False)   
def async_export(email):
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user.type==0:
        campaigns = campaigns = db.session.execute(db.select(Campaign)).scalars()
    else:
        campaigns = db.session.execute(db.select(Campaign).where(Campaign.sponsor_id == user.sponsor.id)).scalars()
    campaigns = [campaign.serialize for campaign in campaigns]

    for i in range(len(campaigns)):
        campaigns[i]['sponsor'] = campaigns[i]['sponsor']['email']
    df = pd.DataFrame(campaigns)
    attachment = "campaigns.csv"
    df.to_csv(f"./instances/{attachment}")

    message = MIMEMultipart()
    message['From'] = env.get('SMTP_EMAIL')
    # message['To'] = email
    # Delete at the end
    message['To'] = "desh.kaiwalya@gmail.com"
    message['Subject'] = "Exported files are Ready!"
    message.attach(MIMEText(f"Hi {user.first_name} {user.last_name},\n"
               "The campaings that you exported are attached with this email.\n"
               "With regards,\n"
               "Connekt"))

    send_mail(attachment=attachment, message=message)

@shared_task(ignore_result=False)
def daily_reminder():
    contracts = db.session.execute(db.select(Contract).where(Contract.status == 2)).scalars()
    for contract in contracts:
        message = MIMEMultipart()
        message['From'] = env.get('SMTP_EMAIL')
        message['To'] = contract.influencer.email
        message['Subject'] = "Exported files are Ready!"
        message.attach(MIMEText(f"Hi {contract.influencer.first_name} {contract.influencer.last_name},\n"
                "You have pending ad requests, visit the website.\n"
                "With regards,\n"
                "Connekt"))
        send_mail(message=message)

@shared_task(ignore_result=False)
def monthly_reminder():
    sponsors = db.session.execute(db.select(User).where(User.flagged == False)).scalars()
    for sponsor in sponsors:
        num_of_campaigns = len(sponsor.sponsor.campaigns)
        num_of_contracts = 0
        total_spent = 0
        influencers = set()
        for campaigns in sponsor.sponsor.campaigns:
            for contract in campaigns.contracts:
                if contract.status == 3:
                    total_spent += contract.payment_amount
                    num_of_contracts += 1
                    influencers.add(contract.influencer.email)
        
        message = MIMEMultipart()
        message['From'] = env.get('SMTP_EMAIL')
        message['To'] = contract.influencer.email
        message['Subject'] = "Exported files are Ready!"
        message.attach(MIMEText(f"Hi {sponsor.first_name} {sponsor.last_name},\n"
                "Your monthly report is here:\n"
                f"Total number of campaigns: {num_of_campaigns}\n"
                f"Total number of contracts: {num_of_contracts}\n"
                f"Total amount on Ads: {total_spent}\n"
                f"Total number of partners: {len(influencers)}\n"
                f"Influencers: {", ".join(influencers)}\n"
                "With regards,\n"
                "Connekt"))
        send_mail(message=message)
