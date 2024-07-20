from flask import Blueprint, jsonify
from database.schema import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks import async_export

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/export")
@jwt_required()
def export():
    """
    Exports the campaigns to CSV files and mails the files
    Only for Admins and Influencers
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if(user.type==0 or user.type==2):
        task = async_export.delay(user.email)
        return jsonify(message="The export has been queued", task_id = task.id), 200

    else:
        return jsonify(message="You do not have access to the campaings"), 403
    
