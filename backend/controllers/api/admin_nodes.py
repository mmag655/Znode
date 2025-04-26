from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi import status
from sqlalchemy.orm import Session
from crud import nodes as crud_nodes
from schemas import nodes as schemas_nodes
from database import get_db
from utils.response import success_response, error_response
from utils.dependencies import get_current_user_id
from crud import users as crud_users

router = APIRouter()

@router.post("/create")
def create_node(node: schemas_nodes.NodeCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None or user.role != "admin":
            return error_response("Unauthorized access", status.HTTP_403_FORBIDDEN)
        
        created = crud_nodes.create_node(db, node)
        return success_response(created.to_dict(), "Node created", status.HTTP_201_CREATED)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/all")
def read_all_nodes(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None or user.role != "admin":
            return error_response("Unauthorized access", status.HTTP_403_FORBIDDEN)
        
        nodes = crud_nodes.get_all_nodes(db)
        node_list = [node.to_dict() for node in nodes]
        return success_response(node_list, "Nodes retrieved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/get/{node_id}")
def read_node(node_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None or user.role != "admin":
            return error_response("Unauthorized access", status.HTTP_403_FORBIDDEN)
        
        node = crud_nodes.get_node(db, node_id)
        if not node:
            return error_response("Node not found", status.HTTP_404_NOT_FOUND)
        return success_response(node.to_dict(), "Node retrieved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.patch("/update/{node_id}")
async def update_node(node_id: int, request: Request, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None or user.role != "admin":
            return error_response("Unauthorized access", status.HTTP_403_FORBIDDEN)

        raw = await request.json()
        node_update = schemas_nodes.NodeUpdate(**raw)
        updated = crud_nodes.update_node(db, node_id, node_update)
        if not updated:
            return error_response("Node not found", status.HTTP_404_NOT_FOUND)
        return success_response(updated.to_dict(), "Node updated")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/delete/{node_id}")
def delete_node(node_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        user = crud_users.get_user(db, user_id)
        if user is None or user.role != "admin":
            return error_response("Unauthorized access", status.HTTP_403_FORBIDDEN)

        deleted = crud_nodes.delete_node(db, node_id)
        if not deleted:
            return error_response("Node not found", status.HTTP_404_NOT_FOUND)
        return success_response(None, "Node deleted")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
