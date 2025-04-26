from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Schema for login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., description="User's raw password")
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
class TokenRequest(BaseModel):
    username: str
    password: str = Field(..., description="User's raw password")
    class Config:
        from_attributes = True
# Schema for signup request
class SignupRequest(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(..., description="User's raw password")
    isAdmin: Optional[bool] = False
    class Config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    email: str
    class Config:
        from_attributes = True

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    class Config:
        from_attributes = True