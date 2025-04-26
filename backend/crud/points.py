from sqlalchemy import Transaction
from sqlalchemy.orm import Session
from utils.redeeme_tokens import send_tokens_to_wallet
from crud.wallet import get_wallet
from models.models import UserPoints
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


def update_user_points(db: Session, user_id: int, updates: UserPointsUpdate):
    try:
        db_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
        if not db_points:
            return None
        for key, value in updates.dict(exclude_unset=True).items():
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
        # Begin a transaction
        with db.begin():  # This ensures all changes are part of the same transaction

            # Fetch user points
            user_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
            if not user_points:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            available_points = user_points.available_for_redemtion
            
            # Check if the user has enough points
            if available_points < points_to_redeem:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough points to redeem")

            # Calculate tokens (assuming 1 point = 1 token)
            factor = 1  # 1 point = 1 token
            tokens_sent = points_to_redeem * factor

            # Update user points for redemption
            user_points.available_for_redemtion -= points_to_redeem
            db.commit()  # This commits the changes to user points

            # Dummy function to send tokens to wallet
            wallet_address = get_wallet(user_id, db)  # Get the user's wallet address

            # Call dummy function to send tokens to wallet
            transaction_successful = send_tokens_to_wallet(wallet_address, tokens_sent)
            
            if not transaction_successful:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send tokens to wallet")

            # Record the transaction
            transaction = Transaction(
                user_id=user_id,
                tokens_redeemed=points_to_redeem,
                transaction_type="redeem",
                transaction_status="completed"
            )
            db.add(transaction)  # Add transaction record to session

            # Commit the transaction to save all changes
            db.commit()  # All changes (points, transaction) are committed to the database
            db.refresh(transaction)
            
            return {
                "total_redeemed_points": points_to_redeem,
                "remaining_points": user_points.available_for_redemtion,
                "transaction_id": transaction.transaction_id,
                "timestamp": transaction.blockchain_timestamp
            }

    except Exception as e:
        db.rollback()  # Rollback the entire transaction if any error occurs
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))