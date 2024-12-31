from web3 import Web3
import json
import pytest

# Connecting to Ganache using Web3
@pytest.fixture(scope = 'module')
def web3():
    rpc_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    assert web3.is_connected(), "Failed to connect to Ganache"
    return web3

# Load contract ABI and bytecode from the compiled contract
@pytest.fixture(scope = 'module')
def voting_contract(web3):
    with open('build/contracts/Voting.json') as f:
        contract_json = json.load(f)
        contract_abi = contract_json['abi']
        contract_bytecode = contract_json['bytecode']

    # Setup deployment account
    private_key = '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7'
    account = web3.eth.account.from_key(private_key)
    web3.eth.default_account = account.address
    print("Address: ", account.address)

    # Deploy the contract
    nonce = web3.eth.get_transaction_count(account.address)
    Voting = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    tx = Voting.constructor().build_transaction({
        "chainId": 1337,
        "gas": 6721975,
        "gasPrice": web3.to_wei('10', 'gwei'),
        "from": account.address,
        "nonce": nonce,
    })
    signed_txn = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi) #Instance
    print("Contract Address: ", contract_address)

# Function to send transactions and wait for receipt
def send_transaction(transaction):
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_hash.hex()}")
    return tx_hash

# # ----------TEST FUNCTIONS----------

# Set voting period
def test_set_voting_period(web3, voting_contract):
    tx = voting_contract.functions.setVotingPeriod(5).transact({'from':web3.eth.default_account})
    web3.eth.wait_for_txn_receipt(tx)
    start_time = voting_contract.functions.startTime().call()
    end_Time = voting_contract.functions.endTime().call()
    assert end_time - start_time == 5 * 60, "Voting period not set correctly"

# # Add candidates
# def test_add_candidates(web3, voting_contract):
#     tx1 = voting_contract.functions.addCandidates('Kirtan').transact({'from':web3.eth.default_account})
    
#     tx2 = voting_contract.functions.addCandidates('Ram').transact({'from':web3.eth.default_account})

#     web3.eth.wait_for_transaction_receipt(tx1)
#     web3.eth.wait_for_transaction_receipt(tx2)
#     count = voting_contract.functions.candidatescount().call()
#     assert count == 2, "Candidate Count mismatch"

# def test_vote_and_get_candidate(web3, voting_contract):
#     tx = voting_contract.functions.vote(1).transact({'from':web3.eth.default_account})
#     web3.eth.wait_for_transaction_receipt(tx)
#     candidate = voting_contract.functions.getCandidate(1).call()
#     assert candidate[2] == 1, "Vote count not updated correctly" 

# # Get total votes (read-only operation)
# def test_get_totals(web3, voting_contract):
#     total_votes_and_candidates = voting_contract.functions.GetTotals().call()
#     assert candidates_count == 2, "Incorrect total candidates"
#     assert candidates_votes == 2, "Incorrect total votes"

# # Get candidate votes (read-only operation)
# def test_get_candidate_votes(web3, voting_contract):
#     get_votes = voting_contract.functions.GetCandidateVotes().call()
#     assert len(candidate_votes) == 2, "Incorrect count of candidates"
#     assert candidate_votes[0][2] == 1, "Incorrect count of votes"
#     assert candidate_votes[1][2] == 0, "Incorrect count of votes" 