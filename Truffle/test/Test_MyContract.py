from web3 import Web3
import pytest
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Update if necessary
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Test Setup
if not web3.is_connected():
    raise ConnectionError("Unable to connect to Ganache")

# Load the compiled contract's ABI and bytecode
with open('build/contracts/MyContract.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']
    contract_bytecode = contract_json['bytecode']

# Accounts and Private Key
accounts = web3.eth.accounts
deployer = accounts[0]
private_key = "0x6ded99b61b32022f6886fd2df37116eabfc488e2dcaa1dbb594d914218394cf6"  # Replace with Ganache's private key for the deployer account

# Deploy the Contract
def deploy_contract():
    MyContract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    txn = MyContract.constructor("Hello, World!").build_transaction({
        'chainId': 1337,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(deployer),
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    return web3.eth.contract(address=txn_receipt.contractAddress, abi=contract_abi)

# Contract instance for testing
def deploy_contract(): 
    return ContractInstance() 

# Test cases
def test_initial_message():
    message = contract_instance.functions.message().call()
    assert message == "Hello, World!", "Initial message is incorrect"

def test_update_message():
    txn = contract_instance.functions.setMessage("New Message").build_transaction({
        'chainId': 1337,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(deployer),
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    web3.eth.waitForTransactionReceipt(txn_hash)

    updated_message = contract_instance.functions.message().call()
    assert updated_message == "New Message", "Message update failed"

def test_unauthorized_update():
    unauthorized_account = accounts[1]
    try:
        txn = contract_instance.functions.setMessage("Unauthorized").buildTransaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': web3.eth.getTransactionCount(unauthorized_account),
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key="0x6ded99b61b32022f6886fd2df37116eabfc488e2dcaa1dbb594d914218394cf6")
        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        pytest.fail("Unauthorized transaction did not revert")
    except Exception as e:
        assert "revert" in str(e), f"Expected revert error, got {str(e)}"