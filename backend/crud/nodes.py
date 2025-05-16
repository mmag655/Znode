from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import Nodes
from schemas import nodes as schemas_nodes

def get_node(db: Session, node_id: int):
    return db.query(Nodes).filter(Nodes.node_id == node_id).first()

def get_node_by_status(db: Session, status: str):
    return db.query(Nodes).filter(Nodes.status == status).first()

def get_all_nodes(db: Session) ->  List[Nodes]:
    return db.query(Nodes).all()

def create_node(db: Session, node: schemas_nodes.NodeCreate):
    db_node = Nodes(
        status=node.status,
        total_nodes=node.total_nodes,
        daily_reward=node.daily_reward
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node

def update_node(db: Session, node_id: int, node_update: schemas_nodes.NodeUpdate):
    db_node = db.query(Nodes).filter(Nodes.node_id == node_id).first()
    if not db_node:
        return None
    update_data = node_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_node, key, value)
    db.commit()
    db.refresh(db_node)
    return db_node

def delete_node(db: Session, node_id: int):
    db_node = db.query(Nodes).filter(Nodes.node_id == node_id).first()
    if not db_node:
        return None
    db.delete(db_node)
    db.commit()
    return True

def adjust_reserved_system_node(db: Session, delta: int, active_assigned: int):
    """
    Adjust reserved system nodes by delta while maintaining total system nodes at 20,000.
    - Positive delta: moves nodes from reserved to active
    - Negative delta: moves nodes from active back to reserved
    - Inactive nodes remain unchanged as the system buffer
    """
    # Get all node categories
    reserved_node = db.query(Nodes).filter(Nodes.status == "reserved").first()
    active_node = db.query(Nodes).filter(Nodes.status == "active").first()
    inactive_node = db.query(Nodes).filter(Nodes.status == "inactive").first()
    
    if not reserved_node or not active_node or not inactive_node:
        raise HTTPException(status_code=404, detail="Required node categories not found")

    # Calculate new totals based on delta direction
    if delta > 0:
        # Moving nodes from reserved to active
        new_reserved = reserved_node.total_nodes - delta
        new_active = active_assigned + delta
        
        # Validate we have enough reserved nodes
        if new_reserved < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough reserved nodes (available: {reserved_node.total_nodes}, requested: {delta})"
            )
    elif delta < 0:
        # Moving nodes from active back to reserved
        new_reserved = reserved_node.total_nodes + abs(delta)
        new_active = active_assigned - abs(delta)
        
        # Validate we have enough active nodes
        if new_active < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough active nodes (available: {active_assigned}, requested: {abs(delta)})"
            )
    else:
        # Delta is zero - no change needed
        return {
            "active_nodes": active_assigned,
            "reserved_nodes": reserved_node.total_nodes,
            "inactive_nodes": inactive_node.total_nodes,
            "message": "No change requested (delta = 0)"
        }

    # Verify total nodes remain at 20,000 (active + reserved + inactive)
    total_after_change = new_active + new_reserved + inactive_node.total_nodes
    if total_after_change != 20000:
        raise HTTPException(
            status_code=400,
            detail=f"System node total must remain at 20,000. Current total would be {total_after_change}"
        )

    # Update reserved nodes
    reserved_update = schemas_nodes.NodeUpdate(
        total_nodes=new_reserved,
        date_updated=datetime.now()
    )
    update_node(db, reserved_node.node_id, reserved_update)
    
    # Update active nodes
    active_update = schemas_nodes.NodeUpdate(
        total_nodes=new_active,
        date_updated=datetime.now()
    )
    update_node(db, active_node.node_id, active_update)
    
    # Return the updated counts
    return {
        "active_nodes": new_active,
        "reserved_nodes": new_reserved,
        "inactive_nodes": inactive_node.total_nodes,
        "message": "Node allocation updated successfully"
    }
