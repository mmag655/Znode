from pydantic import BaseModel
from typing import Optional
import datetime

class UserRewardActivityBase(BaseModel):
    user_id: int
    points: int
    type: Optional[str] = None
    isCredit: Optional[bool] = None
    description: Optional[str] = None
    activity_timestamp: Optional[datetime.datetime] = None

class UserRewardActivityCreate(UserRewardActivityBase):
    pass  # Additional validation for creation can be added here if needed

class UserRewardActivityUpdate(UserRewardActivityBase):
    pass  # Additional validation for update can be added here if needed

class UserRewardActivityResponse(UserRewardActivityBase):
    activity_id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as a dict-like object
