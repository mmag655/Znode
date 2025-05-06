from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models.models import UserNodes
from crud.user_nodes import create_user_node, delete_user_node, get_all_user_nodes, get_user_node, update_user_node
from utils.response import success_response, error_response
from database import get_db
from schemas.user_nodes import UserNodesCreate, UserNodesUpdate, UserNodesOut
from utils.dependencies import get_current_user_id
from typing import List

router = APIRouter()


@router.post("/create")
def create_node(node: UserNodesCreate, db: Session = Depends(get_db)):
    try:
        result = create_user_node(db, node)
        return success_response(result, "UserNode created successfully")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.get("/get")
# def read_all(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
#     try:
#         data = get_all_user_nodes(db, user_id)
#         print("data : ", data)
#         return success_response(UserNodes.to_dict_array(data), "All user nodes retrieved")
#     except Exception as e:
#         return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{user_node_id}")
def read_single(user_node_id: int, db: Session = Depends(get_db)):
    try:
        db_node = get_user_node(db, user_node_id)
        if not db_node:
            return error_response("UserNode not found", status.HTTP_404_NOT_FOUND)
        return success_response(db_node.to_dict(), "UserNode retrieved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/update")
def update_node(updates: UserNodesUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        db_node = update_user_node(db, user_id, updates)
        if not db_node:
            return error_response("UserNode not found", status.HTTP_404_NOT_FOUND)
        return success_response(db_node, "UserNode updated")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_node_id}")
def delete_node(user_node_id: int, db: Session = Depends(get_db)):
    try:
        db_node = delete_user_node(db, user_node_id)
        if not db_node:
            return error_response("UserNode not found", status.HTTP_404_NOT_FOUND)
        return success_response(db_node, "UserNode deleted")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
