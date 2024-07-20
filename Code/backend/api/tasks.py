from flask import Blueprint, jsonify
from database.schema import db, User, Campaign
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks import async_export

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/export")
@jwt_required()
def export():
    """
    Exports the campaigns to CSV files and mails the files
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if(user.type==0):
        campaigns = db.session.execute(db.select(Campaign)).scalars()
        campaigns = [campaign.serialize for campaign in campaigns]
        task = async_export.delay(campaigns, user.email, f"{user.first_name} {user.last_name}")
        return jsonify(message="The export has been queued", task_id = task.id), 200
        
    elif(user.type==2):
        campaigns = db.session.execute(db.select(Campaign).where(Campaign.sponsor_id == user.sponsor.id)).scalars()
        campaigns = [campaign.serialize for campaign in campaigns]
        return jsonify(message="The export has been queued"), 200
    else:
        return jsonify(message="You do not have access to the campaings"), 403
    
