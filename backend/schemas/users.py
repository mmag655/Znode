from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    status: Optional[str] = "active"
    role: Optional[str] = "user"
    
    
class UserCreate(UserBase):
    password: str
    is_first_time_login: Optional[bool] = None
    import_status: Optional[str] = None

class BulkUserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    import_status: Optional[str] = "pending"
    status: Optional[str] = "active"
    assigned_nodes: Optional[int] = 0
    is_first_time_login: Optional[bool] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    role: Optional[str] = None
    is_first_time_login: Optional[bool] = None
    import_status: Optional[str] = None
    
    


class UserOut(UserBase):
    user_id: int
    registration_date: Optional[datetime]
    last_login: Optional[datetime]
    is_first_time_login: Optional[bool]