import json
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import transaction as crud_transaction
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
        print("total transaction: ", len(transactions))
        if not transactions:
            return success_response(data = {}, message="No transactions found")
        # Map the SQLAlchemy model to Pydantic model
        transaction_list = [transaction.to_dict() for transaction in transactions]
        print("transaction_list: ", transaction_list)
        return success_response(transaction_list, "Transaction retrieved")
        
    except Exception as e:
       return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)