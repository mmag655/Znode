# src/crud/wallet.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.models import Wallets
from schemas.wallet import WalletCreate, WalletUpdate

# Create wallet
def create_wallet(user_id: int, wallet_create: WalletCreate, db: Session):
    try:
        # Check if the wallet address already exists
        existing_wallet = db.query(Wallets).filter(Wallets.wallet_address == wallet_create.wallet_address).first()
        if existing_wallet:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wallet address already exists")

        # Create new wallet
        new_wallet = Wallets(
            user_id=user_id,
            wallet_address=wallet_create.wallet_address,
            wallet_type=wallet_create.wallet_type
        )

        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)  # To get the auto-generated fields like wallet_id

        return new_wallet  # Return the created wallet object

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create wallet")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Get wallet by user_id
def get_wallet(user_id: int, db: Session):
    try:
        wallet = db.query(Wallets).filter(Wallets.user_id == user_id).first()
        return wallet
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update wallet
def update_wallet(user_id: int, new_wallet_address: str, db: Session):
    try:
        wallet = db.query(Wallets).filter(Wallets.user_id == user_id).first()

        if not wallet:
            # create a new wallet if it doesn't exist
            wallet = Wallets(
                user_id=user_id,
                wallet_address=new_wallet_address,
                wallet_type="ERC-20"  # Assuming a default type, adjust as necessary
            )
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

        wallet.wallet_address = new_wallet_address  # Actually update it

        db.commit()
        db.refresh(wallet)

        return wallet

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Delete wallet
def delete_wallet(user_id: int, wallet_address: str, db: Session):
    try:
        wallet = db.query(Wallets).filter(Wallets.user_id == user_id, Wallets.wallet_address == wallet_address).first()

        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

        db.delete(wallet)
        db.commit()

        return {"message": "Wallet deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
