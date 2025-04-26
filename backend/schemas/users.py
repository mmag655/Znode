from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    status: Optional[str] = "active"
    role: Optional[str] = "user"
    
    
class UserCreate(UserBase):
    password: str


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