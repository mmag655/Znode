from typing import Dict, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, inspect, text, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Nodes(Base):
    __tablename__ = 'nodes'

    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(Enum('active', 'reserved', 'inactive'))
    total_nodes: Mapped[int] = mapped_column(Integer)
    daily_reward: Mapped[Optional[int]] = mapped_column(Integer)
    date_updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    def to_dict(self) -> Dict:
        return {
            "node_id": self.node_id,
            "status": self.status,
            "total_nodes": self.total_nodes,
            "daily_reward": self.daily_reward,
            "date_updated": self.date_updated.isoformat() if self.date_updated else None
    }
class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('username', name='users_username_key')
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[Optional[str]] = mapped_column(Text)
    registration_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'active'::character varying"))
    role: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'user'::character varying"))
    import_status: Mapped[Optional[str]] = mapped_column(String(20))
    reset_password_token: Mapped[Optional[str]] = mapped_column(Text)
    token_expiry: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    is_first_time_login: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    transactions: Mapped[List['Transactions']] = relationship('Transactions', back_populates='user')
    user_nodes: Mapped[List['UserNodes']] = relationship('UserNodes', back_populates='user')
    user_points: Mapped[List['UserPoints']] = relationship('UserPoints', back_populates='user')
    user_reward_activity: Mapped[List['UserRewardActivity']] = relationship('UserRewardActivity', back_populates='user')
    wallets: Mapped[List['Wallets']] = relationship('Wallets', back_populates='user')
    
    def to_dict(self):
        """Convert User model to dictionary with explicit field handling"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "registration_date": self.registration_date.strftime('%Y-%m-%d %H:%M:%S') if self.registration_date else None,
            "last_login": self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            "status": self.status,
            "role": self.role,
            "import_status": self.import_status,
            "is_first_time_login": self.is_first_time_login
        }


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='transactions_user_id_fkey'),
        PrimaryKeyConstraint('transaction_id', name='transactions_pkey'),
        UniqueConstraint('polygon_tx_hash', name='transactions_polygon_tx_hash_key')
    )

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    tokens_redeemed: Mapped[int] = mapped_column(Integer)
    wallet_address: Mapped[str] = mapped_column(String(255))
    transaction_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    transaction_status: Mapped[Optional[str]] = mapped_column(String(20))
    polygon_tx_hash: Mapped[Optional[str]] = mapped_column(String(255))
    blockchain_timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    blockchain_status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'pending'::character varying"))

    user: Mapped['Users'] = relationship('Users', back_populates='transactions')
    
    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "tokens_redeemed": self.tokens_redeemed,
            "wallet_address": self.wallet_address,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "transaction_status": self.transaction_status,
            "polygon_tx_hash": self.polygon_tx_hash,
            "blockchain_timestamp": self.blockchain_timestamp.isoformat() if self.blockchain_timestamp else None,
            "blockchain_status": self.blockchain_status,
    }


class UserNodes(Base):
    __tablename__ = 'user_nodes'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='user_nodes_user_id_fkey'),
        PrimaryKeyConstraint('user_node_id', name='user_nodes_pkey')
    )

    user_node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    nodes_assigned: Mapped[int] = mapped_column(Integer)
    date_assigned: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='user_nodes')
    
    def to_dict(self):
        return {
            "user_node_id": self.user_node_id,
            "nodes_assigned": self.nodes_assigned,
            "date_assigned": self.date_assigned.strftime('%Y-%m-%d %H:%M:%S') if self.date_assigned else None,
        }

    @staticmethod
    def to_dict_array(nodes: List['UserNodes']) -> List[dict]:
        return [node.to_dict() for node in nodes]

class UserPoints(Base):
    __tablename__ = 'user_points'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='user_points_user_id_fkey'),
        PrimaryKeyConstraint('user_points_id', name='user_points_pkey')
    )

    user_points_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)
    available_for_redemtion: Mapped[int] = mapped_column(Integer)
    zavio_token_rewarded: Mapped[int] = mapped_column(Integer)
    date_updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='user_points')
    
    def to_dict(self):
        return {
            "user_points_id": self.user_points_id,
            "user_id": self.user_id,
            "total_points": self.total_points,
            "available_for_redemtion": float(self.available_for_redemtion) if self.available_for_redemtion is not None else None,
            "zavio_token_rewarded": float(self.zavio_token_rewarded) if self.zavio_token_rewarded is not None else None,
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
        }


class UserRewardActivity(Base):
    __tablename__ = 'user_reward_activity'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='user_reward_activity_user_id_fkey'),
        PrimaryKeyConstraint('activity_id', name='user_reward_activity_pkey')
    )

    activity_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    type: Mapped[Optional[str]] = mapped_column(Enum('reward', 'redemption', 'bonus', name='reward_type'), nullable=True)
    isCredit: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    activity_timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='user_reward_activity')
    
    def to_dict(self):
        return {
            "activity_id": self.activity_id,
            "user_id": self.user_id,
            "points": self.points,
            "type": self.type,
            "isCredit": self.isCredit,
            "description": self.description,
            "activity_timestamp": self.activity_timestamp.isoformat() if self.activity_timestamp else None,
        }



class Wallets(Base):
    __tablename__ = 'wallets'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='wallets_user_id_fkey'),
        PrimaryKeyConstraint('wallet_id', name='wallets_pkey'),
        UniqueConstraint('wallet_address', name='wallets_wallet_address_key')
    )

    wallet_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    wallet_address: Mapped[str] = mapped_column(String(255))
    wallet_type: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='wallets')
    
    def to_dict(self):
        return {
            "wallet_id": self.wallet_id,
            "user_id": self.user_id,
            "wallet_address": self.wallet_address,
            "wallet_type": self.wallet_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

