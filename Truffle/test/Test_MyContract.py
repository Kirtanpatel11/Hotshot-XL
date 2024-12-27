from web3 import Web3
import json

# Connect to the network
rpc_url = "https://endpoints.omniatech.io/v1/bsc/testnet/public"  # Replace with your RPC URL
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check connection
if not web3.is_connected():
    raise ConnectionError("Unable to connect to the network")

# Load the contract ABI and address
with open('build/contracts/MyContract.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']
contract_address = '0xbB5325a9930E9736596C258F72Fe6e87926d7bB9'  # Replace with your contract's address

# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# MetaMask account details
metamask_account = '0xbDC6cC97177301074177800Cba4d518c2Cb473e5'  # Replace with your MetaMask account address

# Call a contract function
def call_contract_function():
    # Function to call - replace 'setMessage' with your actual function name
    function_to_call = contract.functions.setMessage("Hello, Blockchain!")

    # Get the nonce
    nonce = web3.eth.get_transaction_count(metamask_account)

    # Build transaction
    txn = function_to_call.build_transaction({
        'from': metamask_account,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('3', 'gwei'),  # Set gas price to 20 Gwei
    })

    # Print transaction details to sign manually in MetaMask
    print("Sign the following transaction in MetaMask:")
    print(json.dumps(txn, indent=4))
    
    # Wait for user to sign and send the transaction through MetaMask
    tx_hash = input("Enter the transaction hash after signing in MetaMask: ")
    
    # Wait for the transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print("Transaction receipt:", receipt)

# Execute the function call
call_contract_function()
