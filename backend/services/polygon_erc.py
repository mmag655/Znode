import os
from dotenv import load_dotenv
from fastapi import HTTPException
from web3 import Web3
from pydantic import BaseModel
from web3.exceptions import Web3Exception

# Load environment variables (for private key)
load_dotenv()

# Polygon Amoy Testnet Configuration
AMOY_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://rpc-amoy.polygon.technology")  # Official Amoy RPC
w3 = Web3(Web3.HTTPProvider(AMOY_RPC_URL))

# Wallet Configuration (YOUR ADDRESS)
MY_WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "0x167Ad231a26CFFf53D4cBB67c27DBBD727eD39f4")
MY_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")

# Standard ERC-20 ABI
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

class WalletRequest(BaseModel):
    wallet_address: str

class TransferRequest(BaseModel):
    token_address: str
    recipient_address: str
    amount: float

def validate_token_address(token_address: str) -> bool:
    """Check if address is a valid ERC-20 contract"""
    try:
        checksum_addr = Web3.to_checksum_address(token_address)
        contract = w3.eth.contract(address=checksum_addr, abi=ERC20_ABI)
        decimals = contract.functions.decimals().call()
        return True
    except:
        return False

def check_token_balance(wallet: WalletRequest, token_address: str) -> dict:
    try:
        if not w3.is_connected():
            raise Web3Exception("Not connected to Amoy network")
        
        token_address = Web3.to_checksum_address(token_address)
        if not validate_token_address(token_address):
            raise HTTPException(status_code=400, detail="Invalid ERC-20 token")
            
        wallet_address = Web3.to_checksum_address(wallet.wallet_address)
        contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        
        balance = contract.functions.balanceOf(wallet_address).call()
        decimals = contract.functions.decimals().call()
        human_balance = balance / (10 ** decimals)
        
        return {
            "wallet": wallet_address,
            "token": token_address,
            "balance": human_balance,
            "decimals": decimals
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def transfer_tokens(transfer_request: TransferRequest) -> dict:
    try:
        if not w3.is_connected():
            raise Web3Exception("Not connected to Amoy network")
        
        # Validate addresses
        token_address = Web3.to_checksum_address(transfer_request.token_address)
        recipient = Web3.to_checksum_address(transfer_request.recipient_address)
        sender = Web3.to_checksum_address(MY_WALLET_ADDRESS)
        
        if not validate_token_address(token_address):
            raise HTTPException(status_code=400, detail="Invalid token address")
        
        contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        decimals = contract.functions.decimals().call()
        raw_amount = int(transfer_request.amount * (10 ** decimals))
        
        # Check balance
        if contract.functions.balanceOf(sender).call() < raw_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        
        # Build and send transaction
        nonce = w3.eth.get_transaction_count(sender)
        tx = contract.functions.transfer(recipient, raw_amount).build_transaction({
            'chainId': 80002,  # Amoy Testnet chain ID
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, MY_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return {
            "status": "success",
            "tx_hash": tx_hash.hex(),
            "explorer_link": f"https://amoy.polygonscan.com/tx/{tx_hash.hex()}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Example Usage with Amoy Testnet Token
if __name__ == "__main__":
    # Test LINK token on Amoy
    TEST_LINK = "0x0Fd9e8d3aF1aaee056EB9e802c3A762a667b1904"
    
    # 1. Validate token
    print(f"Valid token: {validate_token_address(TEST_LINK)}")
    
    # 2. Check balance
    wallet = WalletRequest(wallet_address=MY_WALLET_ADDRESS)
    print("Balance:", check_token_balance(wallet, TEST_LINK))
    
    # 3. Transfer example (uncomment to test)
    # transfer = TransferRequest(
    #     token_address=TEST_LINK,
    #     recipient_address="0x1FA24452e4C77AE21F75460d7C63eC24AE511491",
    #     amount=1.0  # 1 LINK
    # )
    # print("Transfer:", transfer_tokens(transfer))