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
@router.patch("/admin/approve/")
async def approve_transaction(request: Request, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        # check if user is admin
        raw_body = await request.body()
        body = json.loads(raw_body.decode("utf-8"))
        user = user_crud.get_user(db, user_id)
        if not user.role == "admin":
            return error_response("Unauthorized", status.HTTP_403_FORBIDDEN)
        
        # Approve transaction
        print("transaction_ids : ", body)
        for transaction_id in body["transaction_ids"]:
            transaction = crud_transaction.get_transaction(db, transaction_id)
            if not transaction:
                return error_response("Transaction not found", status.HTTP_404_NOT_FOUND)
            
            # Check if the transaction is already approved
            if transaction.transaction_status == "approved":
                return error_response("Transaction already approved", status.HTTP_400_BAD_REQUEST)
            
            # Approve the transaction
        transaction = crud_transaction.approve_transaction(db, transaction_id)
        if not transaction:
            return error_response("Transaction not found", status.HTTP_404_NOT_FOUND)
        
        return success_response(transaction.to_dict(), "Transaction approved")
    except Exception as e:
       return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)