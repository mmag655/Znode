from sqlalchemy.orm import Session
from models.models import UserRewardActivity
from schemas.activity import UserRewardActivityCreate, UserRewardActivityUpdate

from fastapi import HTTPException, status

from typing import Optional


def create_user_reward_activity(db: Session, user_reward_activity: UserRewardActivityCreate):
    db_activity = UserRewardActivity(
        user_id=user_reward_activity.user_id,
        points=user_reward_activity.points,
        type=user_reward_activity.type,
        isCredit=user_reward_activity.isCredit,
        description=user_reward_activity.description,
        activity_timestamp=user_reward_activity.activity_timestamp,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_user_reward_activity(db: Session, activity_id: int):
    return db.query(UserRewardActivity).filter(UserRewardActivity.activity_id == activity_id).first()


def get_user_reward_activities(db: Session, user_id: int, type: Optional[str] = None):
    try:
        query = db.query(UserRewardActivity).filter(UserRewardActivity.user_id == user_id)
        
        if type:
            query = query.filter(UserRewardActivity.type == type)
        
        activities = query.order_by(UserRewardActivity.activity_timestamp.desc()).all()
        return activities

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch reward activities: {str(e)}"
        )


def update_user_reward_activity(db: Session, activity_id: int, user_reward_activity: UserRewardActivityUpdate):
    db_activity = db.query(UserRewardActivity).filter(UserRewardActivity.activity_id == activity_id).first()
    if db_activity:
        db_activity.user_id = user_reward_activity.user_id
        db_activity.points = user_reward_activity.points
        db_activity.type = user_reward_activity.type
        db_activity.isCredit = user_reward_activity.isCredit
        db_activity.description = user_reward_activity.description
        db_activity.activity_timestamp = user_reward_activity.activity_timestamp
        db.commit()
        db.refresh(db_activity)
        return db_activity
    return None

def delete_user_reward_activity(db: Session, activity_id: int):
    db_activity = db.query(UserRewardActivity).filter(UserRewardActivity.activity_id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return db_activity
    return None
