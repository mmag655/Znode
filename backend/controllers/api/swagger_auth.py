from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from schemas.auth import Token
from services.auth_service import create_access_token, verify_password
from crud.users import get_user_by_email
from database import get_db
from utils.response import error_response


router = APIRouter()

@router.post("/token", response_model=Token)
def token(
    username: str = Form(...),  # Receive username from form data
    password: str = Form(...),  # Receive password from form data
    db: Session = Depends(get_db)  # Dependency for DB session
):
    try:
        user = get_user_by_email(db, username)
        if not user or not verify_password(password, user.password_hash):
            return error_response(message="Invalid credentials", error_code=400)
        
        token = create_access_token({"user_id": user.user_id})
        return Token(access_token=token, token_type="bearer")
    
    except Exception as e:
        # Log the error
        print(f"Error in /token route: {e}")
        
        # Return internal server error response
        return error_response(message="Internal server error", error_code=500)