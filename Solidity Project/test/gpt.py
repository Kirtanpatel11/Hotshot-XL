import pytest
import time
from web3 import Web3
import json

# Sample test file

@pytest.fixture(scope="module")
def web3():
    rpc_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    assert web3.is_connected(), "Failed to connect to Ganache"
    return web3

@pytest.fixture(scope="module")
def contract(web3):
    with open('build/contracts/Voting.json') as f:
        contract_json = json.load(f)
        contract_abi = contract_json['abi']
        contract_bytecode = contract_json['bytecode']

    private_key = '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7'
    account = web3.eth.account.from_key(private_key)
    web3.eth.default_account = account.address

# Deploy the contract
    nonce = web3.eth.get_transaction_count(account.address)

    Voting = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    tx_hash = Voting.constructor().build_transaction({
        "chainId": 1337,
        "gas": 8000000,
        "gasPrice": web3.to_wei('10', 'gwei'),
        "from": account.address,
        "nonce": nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)

    # Use the correct attribute 'raw_transaction'
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress

    voting_contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    return voting_contract

def test_set_voting_period(contract, web3):
    private_key = '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7'
    account = web3.eth.account.from_key(private_key)
    
    tx = contract.functions.setVotingPeriod(10).build_transaction({
        'chainId': 1337,
        'gas': 300000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
        'from': account.address
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)

    start_time = time.time()
    time.sleep(5 * 60)  # Simulate voting period
    end_time = time.time()

    assert end_time - start_time == 5 * 60, "Voting period not set correctly"

# def test_add_candidates(contract, web3):
#     private_key = '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7'
#     account = web3.eth.account.from_key(private_key)

#     candidates = ["Ram", "Datt"]
#     for candidate in candidates:
#         tx = contract.functions.addCandidate(candidate).build_transaction({
#             'chainId': 1337,
#             'gas': 300000,
#             'gasPrice': web3.to_wei('10', 'gwei'),
#             'nonce': web3.eth.get_transaction_count(account.address),
#             'from': account.address
#         })
#         signed_tx = web3.eth.account.sign_transaction(tx, private_key)
#         tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
#         web3.eth.wait_for_transaction_receipt(tx_hash)

#     # Verify candidates
#     for i, candidate in enumerate(candidates, start=1):
#         candidate_info = contract.functions.getCandidate(i).call()
#         assert candidate_info[1] == candidate, f"Candidate {candidate} not added correctly"

# def test_voting(contract, web3):
#     private_key = '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7'
#     account = web3.eth.account.from_key(private_key)

#     tx = contract.functions.vote(1).build_transaction({
#         'chainId': 1337,
#         'gas': 300000,
#         'gasPrice': web3.to_wei('10', 'gwei'),
#         'nonce': web3.eth.get_transaction_count(account.address),
#         'from': account.address
#     })
#     signed_tx = web3.eth.account.sign_transaction(tx, private_key)
#     tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     web3.eth.wait_for_transaction_receipt(tx_hash)

#     # Verify the vote count for the candidate
#     candidate_info = contract.functions.getCandidate(1).call()
#     assert candidate_info[2] == 1, "Vote not counted correctly for the candidate"

# def test_get_totals(contract):
#     total_candidates, total_votes = contract.functions.GetTotals().call()
#     assert total_candidates > 0, "Total candidates should be greater than 0"
#     assert total_votes >= 0, "Total votes should be non-negative"

# def test_get_candidate_votes(contract):
#     candidate_votes = contract.functions.GetCandidateVotes().call()
#     assert len(candidate_votes) > 0, "There should be at least one candidate"
#     for candidate in candidate_votes:
#         print(f"ID: {candidate[0]}, Name: {candidate[1]}, Vote Count: {candidate[2]}")

# # Command to run the tests: pytest test_voting.py
