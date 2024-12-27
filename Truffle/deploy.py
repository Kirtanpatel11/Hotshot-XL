from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not web3.isConnected():
    print("Unable to connect to Ganache")
    exit()

# Load contract details
contract_address = "0x722d72a45475cdC75Fa74791F5C2D3c46bfFd89A"  # Replace with deployed contract address
with open('build/contracts/MyContract.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

# Access the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Read from the contract
message = contract.functions.message().call()
print(f"Message from contract: {message}")

# Write to the contract
private_key = "0x6ded99b61b32022f6886fd2df37116eabfc488e2dcaa1dbb594d914218394cf6"  # Replace with your Ganache private key
account = "0x722d72a45475cdC75Fa74791F5C2D3c46bfFd89A"  # Replace with your Ganache account address

# Build the transaction
txn = contract.functions.setMessage("Hello from Python!").buildTransaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': web3.eth.getTransactionCount(account),
})

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

# Send the transaction
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)
print(f"Transaction receipt: {txn_receipt}")
