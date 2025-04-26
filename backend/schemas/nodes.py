from typing import Optional
from pydantic import BaseModel
import datetime

class NodeBase(BaseModel):
    status: str
    total_nodes: int
    daily_reward: Optional[int] = None

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    status: Optional[str] = None
    total_nodes: Optional[int] = None
    daily_reward: Optional[int] = None
    date_updated: Optional[datetime.datetime] = None

class NodeOut(NodeBase):
    node_id: int
    daily_reward: Optional[int]
    date_updated: Optional[datetime.datetime]

    class Config:
        orm_mode = True
