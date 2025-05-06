# utils/dependencies.py
from fastapi import Depends, HTTPException
import jwt
from sqlalchemy.orm import Session
from database import get_db
from crud.users import get_user
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
        email: str = payload.get("email")
        # verify if user_id is present in db
        print("user_id : ", user_id)
        if user_id is None or email is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if user.email != email:
            raise HTTPException(status_code=401, detail="Unauthorized")
    
    except jwt.ExpiredSignatureError:
        print("JWT Expired Signature Error")
        raise HTTPException(status_code=401, detail="Token has expired")

    except Exception as e:
        print("JWT Decoding Error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    return user_id

