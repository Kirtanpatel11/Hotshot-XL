from web3 import Web3
import json

# Connect to Ethereum network (local Ganache or testnet)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Check connection
if not w3.is_connected():
    raise ConnectionError("Unable to connect to Ganache")

# Load Truffle contract ABI and bytecode
with open('./build/contracts/MyContract.json') as f:
    contract_data = json.load(f)

abi = contract_data['abi']
bytecode = contract_data['bytecode']

# Set up deployment account
account = w3.eth.accounts[0]
w3.eth.default_account = account

# Deploy the contract with the required constructor argument
initial_message = "Hello, Blockchain!"  # Example argument

MyContract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = MyContract.constructor(initial_message).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Print contract address
print(f"Contract deployed at address: {tx_receipt.contractAddress}")
