from typing import Union
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from utils.redeeme_tokens import send_tokens_to_wallet
from crud.wallet import get_wallet
from models.models import Transactions, UserPoints
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
        user_points = (
            db.query(UserPoints)
            .options(joinedload(UserPoints.user))  # Load user relationship
            .all()
        )
        return [
            {
                "id": point.user_points_id,
                "total_points": point.total_points,
                "user_id": point.user_id,
                "user_name": point.user.username,
                "user_email": point.user.email
            }
            for point in user_points
        ]
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
        # Use transaction context manager
        with db.begin():
            # Fetch user points
            user_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
            if not user_points:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            available_points = user_points.available_for_redemtion
            
            if available_points < points_to_redeem:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough points to redeem")

            # Calculate tokens
            factor = 1
            tokens_sent = points_to_redeem * factor

            # Update user points
            user_points.available_for_redemtion -= points_to_redeem
            user_points.zavio_token_rewarded = (user_points.zavio_token_rewarded or 0) + points_to_redeem

            # Get wallet address
            wallet = get_wallet(user_id, db)

            # Send tokens
            transaction_successful = send_tokens_to_wallet(wallet.wallet_address, tokens_sent)
            if not transaction_successful:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send tokens to wallet")

            # Record transaction
            transaction = Transactions(
                user_id=user_id,
                wallet_address=wallet.wallet_address,
                tokens_redeemed=points_to_redeem,
                transaction_status="success"
            )
            db.add(transaction)
            

        # Outside the `with` block: safe to refresh (session is still valid)
        db.refresh(transaction)

        return {
            "total_redeemed_points": points_to_redeem,
            "remaining_points": user_points.available_for_redemtion,
            "transaction_id": transaction.transaction_id,
            "timestamp": transaction.blockchain_timestamp
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
