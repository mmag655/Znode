from datetime import datetime, timezone
from typing import Union
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from utils.timezone import now_gmt5
from crud.wallet import get_wallet
from models.models import Transactions, UserPoints, Users
from schemas.points import UserPointsCreate, UserPointsUpdate
from fastapi import HTTPException, status


def get_user_points(db: Session, user_points_id: int):
    """
    Fetch a single user points record by its ID.
    """
    try:
        return db.query(UserPoints).filter(UserPoints.user_points_id == user_points_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_all_user_points(db: Session, user_id: int):
    try:
        return db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_all_points(db: Session):
    try:
        active_users = db.query(Users).filter(Users.status == "active").all()
        result = []

        for user in active_users:
            user_point = (
                db.query(UserPoints)
                .filter(UserPoints.user_id == user.user_id)
                .first()
            )

            if not user_point:
                # Create an empty UserPoints record for this user
                user_point = UserPoints(user_id=user.user_id, total_points=0, available_for_redemtion=0, zavio_token_rewarded=0)
                db.add(user_point)
                db.commit()
                db.refresh(user_point)

            result.append({
                "id": user_point.user_points_id,
                "total_points": user_point.total_points,
                "available_for_redemption": user_point.available_for_redemtion,
                "user_id": user.user_id,
                "user_name": user.username,
                "user_email": user.email,
                "last_updated": user_point.date_updated.isoformat() if user_point.date_updated else None,
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_user_points(db: Session, points: UserPointsCreate):
    try:
        db_points = UserPoints(**points.dict())
        db.add(db_points)
        db.commit()
        db.refresh(db_points)
        return db_points
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def update_user_points(db: Session, user_id: int, updates: Union[UserPointsUpdate, dict]):
    try:
        db_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
        if not db_points:
            return None

        # Ensure updates is a dict (convert from Pydantic if needed)
        if hasattr(updates, "dict"):
            updates = updates.dict(exclude_unset=True)

        for key, value in updates.items():
            setattr(db_points, key, value)
        db.commit()
        db.refresh(db_points)
        return db_points
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_user_points(db: Session, user_points_id: int):
    try:
        db_points = db.query(UserPoints).filter(UserPoints.user_points_id == user_points_id).first()
        if not db_points:
            return None
        db.delete(db_points)
        db.commit()
        return db_points
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def redeem_user_points(points_to_redeem: int, user_id: int, db: Session):
    try:
        # Fetch user points
        user_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
        if not user_points:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        available_points = user_points.available_for_redemtion
        
        if available_points < points_to_redeem:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough points to redeem")

        # Calculate tokens
        factor = 1  # TODO: Load from env
        tokens_sent = points_to_redeem * factor

        # Update user points
        user_points.available_for_redemtion -= points_to_redeem
        user_points.zavio_token_rewarded = (user_points.zavio_token_rewarded or 0) + points_to_redeem

        # Get wallet address
        wallet = get_wallet(user_id, db)

        # Record transaction
        transaction = Transactions(
            user_id=user_id,
            wallet_address=wallet.wallet_address,
            tokens_redeemed=tokens_sent,
            transaction_status="onhold",
            transaction_date=datetime.now(timezone.utc)
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {
            "total_redeemed_points": points_to_redeem,
            "remaining_points": user_points.available_for_redemtion,
            "transaction_id": transaction.transaction_id,
            "transaction_date": transaction.transaction_date.isoformat() if transaction.transaction_date else None,
        }

    except HTTPException:
        raise  # re-raise HTTP-related errors
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

