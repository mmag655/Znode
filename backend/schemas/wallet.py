# src/schemas/wallet.py

from pydantic import BaseModel
from typing import Optional

class WalletCreate(BaseModel):
    wallet_address: str
    wallet_type: Optional[str] = None

    class Config:
        orm_mode = True

class WalletUpdate(BaseModel):
    wallet_address: Optional[str] = None
    wallet_type: Optional[str] = None

    class Config:
        orm_mode = True

class WalletResponse(BaseModel):
    wallet_id: int
    user_id: int
    wallet_address: str
    wallet_type: Optional[str] = None
    created_at: str

    class Config:
        orm_mode = True
