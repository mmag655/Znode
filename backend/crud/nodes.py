from sqlalchemy.orm import Session
from models.models import Nodes
from schemas import nodes as schemas_nodes

def get_node(db: Session, node_id: int):
    return db.query(Nodes).filter(Nodes.node_id == node_id).first()

def get_node_by_status(db: Session, status: str):
    return db.query(Nodes).filter(Nodes.status == status).first()

def get_all_nodes(db: Session):
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
