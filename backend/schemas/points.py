from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime


class UserPointsBase(BaseModel):
    user_id: int
    nodes_purchased: int
    daily_reward: int
    date_rewarded: Optional[datetime] = None
    class Config:
        from_attributes = True


class UserPointsCreate(UserPointsBase):
    pass


class UserPointsUpdate(BaseModel):
    nodes_purchased: Optional[int] = None
    daily_reward: Optional[int] = None
    date_rewarded: Optional[datetime] = None
    class Config:
        from_attributes = True

    


class UserPointsOut(UserPointsBase):
    user_points_id: int

