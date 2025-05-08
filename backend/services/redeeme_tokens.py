import os
from requests import Session
from crud.users import get_user
from services.smtp_service import get_formatted_fail_email, get_formatted_transfer_email, get_mail_service
from crud.wallet import get_wallet
from database import get_db
from utils.timezone import now_gmt5
from models.models import Transactions
from services.polygon_erc import TransferRequest, transfer_tokens
from dotenv import load_dotenv
load_dotenv()

def send_tokens_to_wallet() -> bool:
    """
    function to simulate sending tokens to a contract.
    In a real-world scenario, this would interact with a blockchain or payment provider.
    """
    try:
        db: Session = next(get_db())
        print(f"⏰ Running transaction(approved) transfer job at {now_gmt5()}")
        
        # Fetch all transactions with "approved" status
        transactions = db.query(Transactions).filter(Transactions.transaction_status == "approved").all()
        
        for transaction in transactions:
            user_id = transaction.user_id
            wallet = get_wallet(user_id, db)
            wallet_address = wallet.wallet_address if wallet else None
            
            if not wallet_address:
                print(f"⚠️ No wallet address found for user {user_id}. Skipping transaction.")
                transaction.transaction_status = "failed"
                transaction.date_updated = now_gmt5()
                db.add(transaction)
                db.commit()  # Commit to database
                continue
            
            tokens_sent = transaction.tokens_redeemed
            
            transfer_request = TransferRequest(
                token_address=os.getenv("TOKEN_CONTRACT_ADDRESS"),
                recipient_address=wallet_address,
                amount=tokens_sent
            )
        
            response = transfer_tokens(transfer_request)
            
            if not response:
                raise ValueError("Failed to send tokens.")

            # Get email service
            email_service = get_mail_service()
            user = get_user(user_id, db)
            
            if response["status"] == "success":
                print(f"Tokens sent successfully to {wallet_address}.")
                transaction.transaction_status = "success"
                transaction.blockchain_timestamp = now_gmt5()
                transaction.polygon_tx_hash = response["tx_hash"]
                # Send success email
                email_service.send_email(
                    subject="Tokens Redeemed Successfully",
                    body=get_formatted_transfer_email(
                        username=user.username,
                        total_token=transaction.tokens_redeemed,
                        link=response["explorer_link"],
                        tx_hash=response["tx_hash"],
                        wallet_address=wallet_address
                    ),
                    from_email="nodes@zaiv.io",
                    to_emails=[user.email],
                    is_html=True
                )
                db.commit()  # Commit the successful transaction update
            else:
                transaction.transaction_status = "failed"
                # Send failure email
                email_service.send_email(
                    subject="Tokens Redeemed Failed",
                    body=get_formatted_fail_email(
                        username=user.username,
                        total_token=transaction.tokens_redeemed,
                        wallet_address=wallet_address
                    ),
                    from_email="nodes@zaiv.io",
                    to_emails=[user.email],
                    is_html=True
                )

            transaction.date_updated = now_gmt5()
            db.add(transaction)
            db.commit()

        return True

    except Exception as e:
        error_message = str(e)
        print(f"Error sending tokens to wallet: {error_message}")
        
        # Send email to admin
        email_service = get_mail_service()
        email_service.send_email(
            subject="Token Transfer Job Failed",
            body=f"""
            <html>
            <body>
                <p>Hi,</p>
                <p><strong>An error occurred during the token transfer job:</strong></p>
                <p><strong>User:</strong> {user.name} ({user.email})</p>
                <p><strong>Wallet Address:</strong> {wallet_address}</p>
                <p><strong>Error Message:</strong> {error_message}</p>
                <p>Please review the issue and take necessary actions.</p>
                <p>Thank you!</p>
                <p><strong>Team ZAIVIO</strong></p>
            </body>
            </html>
            """,
            from_email="nodes@zaiv.io",
            to_emails=["hussain_ce47@yahoo.com"],
            is_html=True
        )
        return False

