from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import decimal


class UserNodesBase(BaseModel):
    user_id: int
    nodes_assigned: int
    class Config:
        from_attributes = True


class UserNodesCreate(UserNodesBase):
    pass


class UserNodesUpdate(BaseModel):
    nodes_assigned: Optional[int] = None
    daily_reward: Optional[decimal.Decimal] = None
    class Config:
        from_attributes = True


class UserNodesOut(UserNodesBase):
    user_node_id: int
    date_assigned: Optional[datetime]
