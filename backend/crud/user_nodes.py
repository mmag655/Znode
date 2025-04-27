from typing import List
from sqlalchemy.orm import Session
from models.models import UserNodes
from schemas.user_nodes import UserNodesCreate, UserNodesUpdate
from fastapi import HTTPException, status


def get_user_node(db: Session, user_id: int):
    try:
        user_nodes = db.query(UserNodes).filter(UserNodes.user_id == user_id).first()
        if user_nodes == None:
            print("No nodes found for user : ", user_id)
        return user_nodes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_all_user_nodes(db: Session, user_id: int) -> List['UserNodes']:
    try:
        user_nodes = db.query(UserNodes).filter(UserNodes.user_id == user_id).all()
        return user_nodes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_user_node(db: Session, node: UserNodesCreate):
    try:
        db_node = UserNodes(**node.model_dump())
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        return db_node
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def update_user_node(db: Session, user_id: int, updates: UserNodesUpdate):
    try:
        db_node = db.query(UserNodes).filter(UserNodes.user_id == user_id).first()
        if not db_node:
            return None
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_node, key, value)
        db.commit()
        db.refresh(db_node)
        return db_node
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_user_node(db: Session, user_node_id: int):
    try:
        db_node = db.query(UserNodes).filter(UserNodes.user_node_id == user_node_id).first()
        if not db_node:
            return None
        db.delete(db_node)
        db.commit()
        return db_node
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
