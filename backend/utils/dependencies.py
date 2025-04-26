# utils/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from services.auth_service import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

def get_current_user_id(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print("token", token)
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    try:
        payload = decode_jwt_token(token)
        print("Decoded Payload:", payload)
        user_id: int = payload.get("user_id")
        print("user_id : ", user_id)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

    except Exception as e:
        print("JWT Decoding Error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    return user_id

