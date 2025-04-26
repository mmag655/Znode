# src/schemas/transaction.py

from pydantic import BaseModel
from typing import Optional
import datetime

class TransactionBase(BaseModel):
    user_id: int
    tokens_redeemed: int
    wallet_address: str
    transaction_status: Optional[str] = "completed"
    transaction_date: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True

class TransactionResponse(TransactionBase):
    transaction_id: int
    transaction_date: datetime.datetime

class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]

