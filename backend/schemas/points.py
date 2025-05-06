from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserPointsBase(BaseModel):
    user_id: int
    total_points: int
    available_for_redemtion: int
    zavio_token_rewarded: int
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPointsCreate(UserPointsBase):
    pass


class UserPointsUpdate(BaseModel):
    total_points: Optional[int] = None
    available_for_redemtion: Optional[int] = None
    zavio_token_rewarded: Optional[int] = None
    date_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPointsOut(UserPointsBase):
    user_points_id: int
