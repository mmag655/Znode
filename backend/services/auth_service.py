import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import bcrypt
import jwt
from fastapi import HTTPException

# Secret key for JWT generation
SECRET_KEY = os.getenv("SECRET_KEY", "slaxseewoi3786sa87esuakdaskjdhiewriudhkjsauklCnasiifh")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))



# Function to create JWT token
def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Use timezone-aware UTC datetime
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default expiry time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to create a refresh token
def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to hash a password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to verify a password
def verify_password(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))


# Function to decode JWT token and extract user_id
def decode_jwt_token(token: str, refresh_required=False) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID not found in token")

        if refresh_required and payload.get("type") != "refresh":
            raise HTTPException(status_code=403, detail="Invalid token type for refreshing")

        expiration_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        if expiration_time < datetime.now(timezone.utc):
            raise jwt.ExpiredSignatureError  # Explicitly raise for handling below

        return payload

    except jwt.ExpiredSignatureError:
        if refresh_required:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        else:
            raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.PyJWTError as e:
        print("JWT erorr : ", e)
        raise HTTPException(status_code=401, detail="Invalid token")

def create_reset_token(email: str) -> str:
    """Generate a password reset token."""
    expire = datetime.now() + timedelta(hours=1)
    to_encode = {"email": email}
    to_encode.update({"exp": expire, "type": "reset_password"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_email_token(token: str) -> str:
    """Decode the reset token and return the email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "reset_password":
            raise ValueError("Invalid token type")
        return payload
    except jwt.PyJWTError as e:
        raise ValueError(f"Token decoding failed: {e}")


