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
    
@tasks_bp.route('dashboard')
@jwt_required()
def dashboard():
    """
    Sends statistics to the admin
    """
    user = db.session.execute(db.select(User).where(User.email == get_jwt_identity())).scalar()
    if(user.type != 0):
        return jsonify(message="You do not have access to this information"), 403
    
    stat = dict()
    stat['ActiveUsers'] = dict()
    stat['NichexIndustry'] = dict()
    stat['ActiveUsers']['total'] = [0,0]
    stat['ActiveUsers']['active'] = [0,0]
    stat['NichexIndustry']['niche'] = [0,0,0,0]
    stat['NichexIndustry']['industry'] = [0,0,0,0]
    for user in db.session.execute(db.select(User)).scalars().all():
        if user.type == 1:
            stat['ActiveUsers']['total'][0] += 1
            if not user.flagged:
                stat['ActiveUsers']['active'][0] += 1

            counter = {'Healthcare':0, 'Gaming':1, 'Tech':2, 'Vlog':3}
            stat['NichexIndustry']['niche'][counter[user.influencer.niche]] += 1
                
        elif user.type == 2:
            stat['ActiveUsers']['total'][1] += 1
            if not user.flagged:
                stat['ActiveUsers']['active'][1] += 1

            counter = {'Healthcare':0, 'Gaming':1, 'Tech':2, 'Vlog':3}
            stat['NichexIndustry']['industry'][counter[user.sponsor.industry]] += 1

    stat['ContractxPlatform']=[0, 0, 0, 0]
    for user in db.session.execute(db.select(User).where(User.type == 1)).scalars().all():
        counter = {'Youtube':0, 'Tiktok':1, 'Instagram':2, 'Twitter':3}
        stat['ContractxPlatform'][counter[user.influencer.platform]] += len(user.influencer.contracts)

    stat['BudgetxIndustry'] = dict()
    stat['BudgetxIndustry']['budget'] = [0,0,0,0]
    stat['BudgetxIndustry']['actual_spent'] = [0,0,0,0]
    for user in db.session.execute(db.select(User).where(User.type == 2)).scalars().all():
        counter = {'Healthcare':0, 'Gaming':1, 'Tech':2, 'Vlog':3}
        for campaign in user.sponsor.campaigns:
            stat['BudgetxIndustry']['budget'][counter[user.sponsor.industry]] += user.sponsor.budget
            if campaign.approved:
                for contract in campaign.contracts:
                    if contract.status == 3:
                         stat['BudgetxIndustry']['actual_spent'][counter[user.sponsor.industry]] += contract.payment_amount

    return jsonify(stat), 200