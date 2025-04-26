# src/controllers/wallet.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.dependencies import get_current_user_id
from schemas.wallet import WalletCreate, WalletUpdate, WalletResponse
from crud.wallet import create_wallet, get_wallet, update_wallet, delete_wallet
from database import get_db  # Assuming you have a dependency to get the DB session
from utils.response import success_response, error_response

router = APIRouter()

# Create Wallet
@router.post("/create_wallet", response_model=WalletResponse)
def create_wallet_view(wallet_create: WalletCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        wallet = create_wallet(user_id, wallet_create, db)
        return success_response(wallet.to_dict(), "Wallet created successfully")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get Wallet
@router.get("/get_wallet", response_model=WalletResponse)
def get_wallet_view(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        wallet = get_wallet(user_id, db)
        if not wallet:
            return success_response(data={}, message="Wallet not found")
        return success_response(wallet.to_dict(), "Wallet fetched successfully")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update Wallet
@router.put("/update_wallet", response_model=WalletResponse)
def update_wallet_view(wallet_address: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        updated_wallet = update_wallet(user_id, wallet_address, db)
        return success_response(updated_wallet.to_dict(), "Wallet updated successfully")
    except HTTPException as e:
        return error_response(e.detail, e.status_code)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete Wallet
@router.delete("/delete_wallet")
def delete_wallet_view(wallet_address: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        delete_wallet(user_id, wallet_address, db)
        return success_response(None, "Wallet deleted successfully", status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        return error_response(e.detail, e.status_code)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
