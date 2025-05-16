from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from schemas.nodes import NodeUpdate
from models.models import UserNodes
from schemas.user_nodes import UserNodesCreate, UserNodesUpdate
import crud.nodes as system_nodes
from fastapi import HTTPException, status


def get_user_node(db: Session, user_id: int):
    try:
        user_nodes = db.query(UserNodes).filter(UserNodes.user_id == user_id).first()
        if user_nodes == None:
            print("No nodes found for user : ", user_id)
        return user_nodes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_all_user_nodes(db: Session) -> List['UserNodes']:
    try:
        user_nodes = db.query(UserNodes).filter().all()
        return user_nodes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_sum_assigned_all(db: Session) -> float:
    try:
        # Get sum of nodes_assigned column instead of count
        total_nodes = db.query(func.sum(UserNodes.nodes_assigned)).scalar()
        # Return 0 if no records found (scalar() returns None in that case)
        return float(total_nodes) if total_nodes is not None else 0.0
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
def create_user_node(db: Session, node: UserNodesCreate):
    try:
        all_system_nodes = system_nodes.get_all_nodes(db)
        active_assigned_count = get_sum_assigned_all(db)
        all_available = sum(n.total_nodes for n in all_system_nodes)

        if active_assigned_count + node.nodes_assigned > all_available:
            return None

        system_nodes.adjust_reserved_system_node(db, delta=node.nodes_assigned, active_assigned=active_assigned_count)

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
        
        all_system_nodes = system_nodes.get_all_nodes(db)
        active_assigned_count = get_sum_assigned_all(db)
        all_available = sum(n.total_nodes for n in all_system_nodes)

        if active_assigned_count + updates.nodes_assigned > all_available:
            return None


        update_data = updates.model_dump(exclude_unset=True)

        # Validate and adjust node count safely
        if 'nodes_assigned' in update_data:
            old_value = db_node.nodes_assigned
            new_value = update_data['nodes_assigned']

            if new_value < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Assigned nodes cannot be negative."
                )

            delta = new_value - old_value

            # Prevent reduction below current usage
            if delta < 0 and abs(delta) > old_value:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot reduce assigned nodes below current value ({old_value})."
                )

            if delta != 0:
                system_nodes.adjust_reserved_system_node(db, delta=delta, active_assigned=active_assigned_count)

        # Update other fields
        for key, value in update_data.items():
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
