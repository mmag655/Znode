import json
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import transaction as crud_transaction, users as user_crud
from schemas import transaction as schemas_transaction
from database import get_db
from utils.response import success_response, error_response
from fastapi import status
from utils.dependencies import get_current_user_id

#default pass "dp_IMPASS"

router = APIRouter()

@router.get("/all")
def read_transactions(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        # Get all transactions
        transactions = crud_transaction.get_transactions(user_id, db)
        if not transactions:
            return success_response(data = {}, message="No transactions found")
        # Map the SQLAlchemy model to Pydantic model
        transaction_list = [transaction.to_dict() for transaction in transactions]
        return success_response(transaction_list, "Transaction retrieved")
        
    except Exception as e:
       return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/admin/all")
def read_admin_transactions(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        # check if user is admin
        user = user_crud.get_user(db, user_id)
        if not user.role == "admin":
            return error_response("Unauthorized", status.HTTP_403_FORBIDDEN)
        
        # Get all transactions
        transaction_list = crud_transaction.get_all_onhold_transactions(db)
       
        if not transaction_list:
            return success_response(data = {}, message="No transactions found")
        # Map the SQLAlchemy model to Pydantic model
       
        return success_response(transaction_list, "Transaction retrieved")
        
    except Exception as e:
       return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.patch("/admin/approve")
async def approve_transaction(request: Request, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        # Parse request body
        raw_body = await request.body()
        body = json.loads(raw_body.decode("utf-8"))
        transaction_ids = body.get("transaction_ids", [])

        # Validate admin role
        user = user_crud.get_user(db, user_id)
        if not user or user.role != "admin":
            return error_response("Unauthorized", status.HTTP_403_FORBIDDEN)

        approved_transactions = []
        
        for transaction_id in transaction_ids:
            transaction = crud_transaction.get_transaction(db, transaction_id)
            if not transaction:
                return error_response(f"Transaction ID {transaction_id} not found", status.HTTP_404_NOT_FOUND)

            if transaction.transaction_status == "approved":
                return error_response(f"Transaction ID {transaction_id} already approved", status.HTTP_400_BAD_REQUEST)

            # Approve transaction
            approved = crud_transaction.approve_transaction(db, transaction_id)
            if not approved:
                return error_response(f"Transaction ID {transaction_id} could not be approved", status.HTTP_500_INTERNAL_SERVER_ERROR)

            approved_transactions.append(approved.to_dict())

        return success_response(approved_transactions, "Transactions approved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
