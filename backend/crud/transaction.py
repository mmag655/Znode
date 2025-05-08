# src/crud/transaction.py

from datetime import datetime
from sqlalchemy.orm import Session
from utils.timezone import now_gmt5
from models.models import Transactions, Users

#Function to fetch a single transaction by ID
def get_transaction(db: Session, transaction_id: int):
    try:
        # Fetch the transaction by ID
        transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
        if not transaction:
            print(f"Transaction with ID {transaction_id} not found.")
            return None
        return transaction
    except Exception as e:
        # Handle any exceptions that occur during the query
        print(f"Error fetching transaction with ID {transaction_id}: {e}")
        return None

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

def get_all_onhold_transactions(db: Session):
    try:
        # Fetch transactions for the given user_id
        transactions = db.query(
            Transactions,
            Users.username,
            Users.email
        ).join(
            Users, Transactions.user_id == Users.user_id
        ).order_by(Transactions.transaction_date.desc()
        ).all()
        # Convert the result to a list of dictionaries
        transaction_list = []
        for txn, username, email in transactions:
            transaction_list.append({
                "transaction_id": txn.transaction_id,
                "user_id": txn.user_id,
                "user_name": username,
                "user_email": email,
                "tokens_redeemed": txn.tokens_redeemed,
                "transaction_date": txn.transaction_date.isoformat() if txn.transaction_date else None,
                "transaction_status": txn.transaction_status,
                "blockchain_status": txn.blockchain_status,

            })

        return transaction_list 
    except Exception as e:
        # Handle any exceptions that occur during the query
        print(f"Error fetching transactions : {e}")
        return []
    
def approve_transaction(db: Session, transaction_id: int):
    try:
        # Fetch the transaction by ID
        transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
        if not transaction:
            print(f"Transaction with ID {transaction_id} not found.")
            return None

        # Update the transaction status
        transaction.transaction_status = 'approved'
        transaction.transaction_date = now_gmt5()
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception as e:
        # Handle any exceptions that occur during the update
        print(f"Error approving transaction with ID {transaction_id}: {e}")
        db.rollback()
        return None
        
# Function to create a new transaction
# def create_transaction(user_id: int, transaction_data: dict, db: Session):
#     try:
#         # Create a new transaction object
#         new_transaction = Transactions(
#             user_id=user_id,
#             **transaction_data
#         )
#         # Add the new transaction to the session
#         db.add(new_transaction)
#         # Commit the session to save the transaction to the database
#         db.commit()
#         # Refresh the session to get the latest data
#         db.refresh(new_transaction)
#         return new_transaction
#     except Exception as e:
#         # Handle any exceptions that occur during the transaction creation
#         print(f"Error creating transaction for user_id {user_id}: {e}")
#         db.rollback()
#         return None
