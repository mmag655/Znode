import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status

from sqlalchemy.orm import Session
from utils.dependencies import get_current_user_id
from schemas.auth import ForgotPasswordRequest, LoginRequest, ResetPasswordRequest, SignupRequest, TokenRequest, Token
from services.auth_service import create_access_token, create_refresh_token, create_reset_token, decode_email_token, decode_jwt_token, verify_password, hash_password
from crud.users import create_user, get_user, get_user_by_email, update_user_password
from database import get_db
from utils.response import success_response, error_response
from utils.logging_config import logger
import jwt

router = APIRouter()

# Signup route with try-except
@router.post("/signup")
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    try:
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            # Return an error response in the expected format if email is already registered
            return error_response(message="Email already registered", error_code=400)
        
        print(f"Creating user : {user_data.model_dump_json()}")
        
        hashed_password = hash_password(user_data.password)
        
        # Assign the hashed password to the user data before creating the user
        user_data.password = hashed_password
        create_user(db, user_data)
        
        return success_response(data={"email": user_data.email}, message="User registered successfully")
    
    except Exception as e:
        # Log the error (optional, depending on your logging setup)
        print(f"Error in signup: {e}")
        
        return error_response(message="Internal server error", error_code=500)

@router.post("/login")
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, user_data.email)
        
        if not user:
            return error_response(
                message="No account found with this email",
                error_code=status.HTTP_401_UNAUTHORIZED
            )
            
        if not verify_password(user_data.password, user.password_hash):
            return error_response(
                message="Incorrect password",
                error_code=status.HTTP_401_UNAUTHORIZED
            )
        
        access_token = create_access_token({"user_id": user.user_id, "email": user.email})
        refresh_token = create_refresh_token({"user_id": user.user_id, "email": user.email})
        
        # Set refresh token as HttpOnly cookie
        response = success_response(
            data={
                "access_token": access_token,
                "token_type": "bearer"
            }
        )
        # Set refresh token as secure, HttpOnly cookie
        # response.set_cookie(
        #     key="refresh_token",
        #     value=refresh_token,
        #     httponly=True,
        #     secure=True,
        #     samesite="none",
        #     max_age=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)) * 86400,
        #     path="/",
        #     domain=".zaiv.io"
        # )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # ✅ Allow HTTP during development
            samesite="lax",  # ✅ Prevent cross-site issues
            max_age=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)) * 86400,
            path="/",
        )
        return response
    except Exception as e:
        print(f"Error in login: {e}")
        return error_response(message="Internal server error", error_code=500)

@router.post("/logout")
def logout(response: Response):
    try:
        # Remove the refresh token by setting it to an empty value and expiring it
        response.delete_cookie(
            key="refresh_token",
            # domain=".zaiv.io",
            path="/"
        )

        # ✅ Return the response correctly
        return success_response(data={"message": "Logged out successfully"})

    except Exception as e:
        print(f"Error in logout: {e}")
        return error_response(message="Internal server error", error_code=500)


@router.post("/token/refresh")
def refresh_token_route(request: Request, db: Session = Depends(get_db)):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return error_response(message="Refresh token missing", error_code=401)

        try:
            payload = decode_jwt_token(refresh_token, refresh_required=True)
        except jwt.ExpiredSignatureError:
            return error_response(message="Refresh token expired", error_code=401)
        except jwt.InvalidTokenError:
            return error_response(message="Invalid refresh token", error_code=401)

        user_id = payload.get("user_id")
        new_access_token = create_access_token({"user_id": user_id})

        return success_response(data={"access_token": new_access_token, "token_type": "bearer"})

    except Exception as e:
        print("Error:", e)
        return error_response(message="Internal server error", error_code=500)

@router.post("/auth/token/verify")
def verify_token(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Verify the token and return user details, including subscription status."""
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            return error_response(message="User not found", error_code=204)

        return success_response(
            data={
                "user_id": user_id,
            },
            message="Success"
        )

    except Exception as e:
        logger.error(f"Error verifying token: {e}", exc_info=True)
        return error_response(message="Internal server error", error_code=500)


    
@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Generate reset token and return it to the frontend."""
    user = get_user_by_email(db, request.email)
    if not user:
        return error_response(message="User not found", error_code=204)

    reset_token = create_reset_token(request.email)
    
    return success_response(data={"reset_token": reset_token}, message="Use this token to reset the password")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Verify token and reset password."""
    try:
        print("request : ", request.model_dump_json())
        payload = decode_email_token(request.token)
        email = payload.get("email")
    except HTTPException:
        return error_response(message="Invalid or expired token", error_code=400)

    user = get_user_by_email(db, email)
    if not user:
        return error_response(message="User not found", error_code=204)

    hashed_password = hash_password(request.new_password)
    updated_user = update_user_password(db, user.user_id, hashed_password)
    if not updated_user:
        return error_response(message="Failed to update password", error_code=500)

    return success_response(data={"message": "Password updated successfully"}, message="Password updated successfully")