# src/crud/transaction.py

from sqlalchemy.orm import Session
from models.models import Transactions

# Function to fetch user transactions
def get_transactions(user_id: int, db: Session):
    try:
        # Fetch transactions for the given user_id
        transactions = db.query(Transactions).filter(Transactions.user_id == user_id).all()
        return transactions
    except Exception as e:
        # Handle any exceptions that occur during the query
        print(f"Error fetching transactions for user_id {user_id}: {e}")
        return []
# Function to create a new transaction
def create_transaction(user_id: int, transaction_data: dict, db: Session):
    try:
        # Create a new transaction object
        new_transaction = Transactions(
            user_id=user_id,
            **transaction_data
        )
        # Add the new transaction to the session
        db.add(new_transaction)
        # Commit the session to save the transaction to the database
        db.commit()
        # Refresh the session to get the latest data
        db.refresh(new_transaction)
        return new_transaction
    except Exception as e:
        # Handle any exceptions that occur during the transaction creation
        print(f"Error creating transaction for user_id {user_id}: {e}")
        db.rollback()
        return None
