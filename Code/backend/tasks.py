from celery import Celery, Task, shared_task
from flask import Flask

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
def async_export(campaigns, email, name):
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
    message.attach(MIMEText(f"Hi {name},\n"
               "The campaings that you exported are attached with this email.\n"
               "With regards,\n"
               "Connekt"))

    send_mail(attachment=attachment, message=message)
