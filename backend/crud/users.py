from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Users
from schemas.users import UserCreate, UserUpdate
from passlib.hash import bcrypt


def get_user(db: Session, user_id: int):
    try:
        return db.query(Users).filter(Users.user_id == user_id).first()
    except SQLAlchemyError as e:
        print(f"Error in get_user: {e}")
        return None


def get_user_by_email(db: Session, email: str):
    try:
        return db.query(Users).filter(Users.email == email).first()
    except SQLAlchemyError as e:
        print(f"Error in get_user_by_email: {e}")
        return None


def get_users(db: Session):
    try:
        return db.query(Users).all()
    except SQLAlchemyError as e:
        print(f"Error in get_users: {e}")
        return []


def create_user(db: Session, user: UserCreate):
    try:
        db_user = Users(
            username=user.username,
            email=user.email,
            password_hash=user.password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error in create_user: {e}")
        return None


def update_user(db: Session, user_id: int, user: UserUpdate):
    try:
        db_user = db.query(Users).filter(Users.user_id == user_id).first()
        if not db_user:
            return None
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error in update_user: {e}")
        return None
    
def update_user_password(db: Session, user_id: int, password_hash: str):
    try:
        db_user = db.query(Users).filter(Users.user_id == user_id).first()
        if not db_user:
            print(f"User with ID {user_id} not found")
            return None
            
        
        db_user.password_hash = password_hash
        db.commit()
        
        # Verify the update
        db.refresh(db_user)
        
        if db_user.password_hash != password_hash:
            print("Update did not persist!")
            return None
        
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error in update_user_password: {e}")
        return None
     
def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(Users).filter(Users.user_id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error in delete_user: {e}")
        return None
