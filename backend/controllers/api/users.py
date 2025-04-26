import json
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import users as crud_users
from crud import user_nodes as crud_nodes
from schemas import users as schemas_users
from database import get_db
from utils.response import success_response, error_response
from fastapi import status
from utils.dependencies import get_current_user_id

#default pass "dp_IMPASS"

router = APIRouter()

@router.post("/create")
def create_user(user: schemas_users.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud_users.get_user_by_email(db, user.email)
        if db_user:
            return error_response("Email already registered", status.HTTP_400_BAD_REQUEST)
        created = crud_users.create_user(db, user)
        return success_response(created.to_dict(), "User created", status.HTTP_201_CREATED)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/all")
def read_users(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)
        if not user.role == "admin":
            return error_response("You are not authorized to view all users", status.HTTP_403_FORBIDDEN)
        # Get all users
        users = crud_users.get_users(db)  # SQLAlchemy model instances
        print("total user: ", len(users))
        # get nodes for each user

        # Map the SQLAlchemy model to Pydantic model
        user_list = [user.to_dict() for user in users]
        
        for item in user_list:
            # print(item)
            nodes = crud_nodes.get_user_node(db, item['user_id'])
            if nodes:
                item['assigned_nodes'] = nodes.nodes_assigned
            else:
                item['assigned_nodes'] = 0
        
        print("user_list: ", user_list)
        return success_response(user_list, "User retrieved")
        
    except Exception as e:
       return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/get")
def read_user(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if not user:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)
        return success_response(user.to_dict(), "User retrieved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.patch("/update")
async def update_user(request: Request, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        raw = await request.json()  
        print("🔍 Raw body received:", raw)
        user = schemas_users.UserUpdate(**raw)    
        updated = crud_users.update_user(db, user_id, user)
        if not updated:
            return error_response("User not found", status.HTTP_403_FORBIDDEN)
        return success_response(updated.to_dict(), "User updated")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/id/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        deleted = crud_users.delete_user(db, user_id)
        if not deleted:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)
        return success_response(None, "User deleted")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
