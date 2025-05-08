import json
from sqlite3 import IntegrityError
from typing import Any, Dict, List
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from services.smtp_service import get_mail_service, get_zaivio_welcome_email
from services.auth_service import hash_password
from schemas.user_nodes import UserNodesCreate, UserNodesUpdate
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
def create_user(user: schemas_users.UserCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)
        if not user.role == "admin":
            return error_response("You are not authorized to view all users", status.HTTP_403_FORBIDDEN)
        
        db_user = crud_users.get_user_by_email(db, user.email)
        if db_user:
            return error_response("Email already registered", status.HTTP_400_BAD_REQUEST)
        created = crud_users.create_user(db, user)
        return success_response(created.to_dict(), "User created", status.HTTP_201_CREATED)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/bulk/create", status_code=status.HTTP_207_MULTI_STATUS ) 
async def bulk_create_users(request: Request, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    success: List[Dict] = []
    failed: List[Dict] = []
    
    try:
        user = crud_users.get_user(db, user_id)
        if user is None:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)
        if not user.role == "admin":
            return error_response("You are not authorized to view all users", status.HTTP_403_FORBIDDEN)
        
        users_data = await request.json()
        
        for user_data in users_data:
            try:
                # Check if user exists (using existing CRUD function)
                print("user_data: ", user_data)
                
                if crud_users.get_user_by_email(db, user_data["email"]):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already exists"
                    )
                # Create user (using existing CRUD function)
                # username = user_data.get("username")
                password = user_data.get("password", f"{user_data['username'][:3]}Xrbnh@123")
                hashed_password = hash_password(password)
                user_data["password"] = hashed_password
                
                userToCreate = schemas_users.BulkUserCreate(**user_data)
                created_user = crud_users.create_user(db, userToCreate)
                if created_user is not None:
                    success.append({
                        "email": created_user.email,
                        "user_id": created_user.user_id,
                        "name": f"{created_user.username}"
                    })
                    # Send welcome email
                    email_service = get_mail_service()
                    email_service.send_email(
                        subject="Welcome to ZAIVIO Nodes",
                        body=get_zaivio_welcome_email(user_data["username"], password=password),
                        from_email="nodes@zaiv.io",
                        to_emails=[user_data["email"]],
                        is_html=True
                    )
                # Create user node if nodes are provided
                if user_data["assigned_nodes"] > 0:
                    node_data = UserNodesCreate(
                        user_id=created_user.user_id,
                        nodes_assigned=user_data["assigned_nodes"]
                    )
                    crud_nodes.create_user_node(db, node_data)
                else:
                    # Create a default node if no nodes are provided
                    node_data = UserNodesCreate(
                        user_id=created_user.user_id,
                        nodes_assigned=0
                    )
                    crud_nodes.create_user_node(db, node_data)
                # Commit the transaction for each user
                
            except HTTPException as e:
                print("HTTPException: ", e)
                failed.append({
                    "username": user_data["username"],
                    "error": e.detail,
                    "code": e.status_code
                })
            except IntegrityError as e:
                print("IntegrityError: ", e)
                failed.append({
                    "username": user_data["username"],
                    "error": "Database integrity error (e.g., duplicate)",
                    "code": status.HTTP_400_BAD_REQUEST
                })
            except Exception as e:
                print("Exception: ", e)
                failed.append({
                    "username": user_data["username"],
                    "error": str(e),
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR
                })
        
        
    except Exception as e:
        print("Error in bulk_create_users:", e)
        db.rollback()
        return error_response(message={
            "status": "transaction_failed",
            "error": str(e),
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return success_response(data={
        "success": success,
        "failed": failed,
        "summary": {
            "total": len(users_data),
            "succeeded": len(success),
            "failed": len(failed)
        }
    }, message="Bulk user creation completed")
    
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
        
        # print("user_list: ", user_list)
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

@router.patch("/suspend/{userId}")
def suspend_user(userId: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None:
            return error_response("Admin user not found", status.HTTP_404_NOT_FOUND)
        if not user.role == "admin":
            return error_response("You are not authorized to suspend users", status.HTTP_403_FORBIDDEN)
        user_to_update = crud_users.get_user(db, userId)
        if user_to_update is None:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)
        # Check if the user is already suspended
        if user_to_update.status == "inactive":
            user_to_update.status = "active"
        else:
            user_to_update.status = "inactive"
            
        user = schemas_users.UserUpdate(
            user_id=userId,
            status=user_to_update.status
        )
        user = crud_users.update_user(db, userId, user)
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
        
        update_data = raw.copy()
        target_user_id = raw.get("user_id", user_id)
        
        # Handle nodes update if present
        if "nodes" in raw:
            # check if admin
            user = crud_users.get_user(db, user_id)
            if user is None:
                return error_response("User not found", status.HTTP_404_NOT_FOUND)
            if not user.role == "admin":
                return error_response("You are not authorized to update users", status.HTTP_403_FORBIDDEN)
            
            nodes = crud_nodes.get_user_node(db, target_user_id)
            if nodes:
                update_node_data = UserNodesUpdate(
                    user_id=target_user_id,
                    nodes_assigned=raw["nodes"]
                )
                crud_nodes.update_user_node(db, target_user_id, update_node_data)
            else:
                node_data = UserNodesCreate(
                user_id=target_user_id,
                nodes_assigned=raw["nodes"]  # Ensure this matches the expected type (e.g., str, list, etc.)
                )
                print("node_data: ", node_data)
                crud_nodes.create_user_node(db, node_data)
            
            del update_data["nodes"]
            
        print("update_data: ", update_data)
        # Remove user_id from update data if present
        if "user_id" in update_data:
            del update_data["user_id"]
        
        user = schemas_users.UserUpdate(**update_data)    
        updated = crud_users.update_user(db, target_user_id, user)
        if not updated:
            return error_response("User not found", status.HTTP_404_NOT_FOUND)  # Changed from 403 to 404
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
