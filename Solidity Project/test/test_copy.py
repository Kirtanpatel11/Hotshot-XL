from web3 import Web3
import json
import pytest

# Connecting to Ganache using Web3
@pytest.fixture(scope='module')
def web3():
    rpc_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    assert web3.is_connected(), "Failed to connect to Ganache"
    return web3

# Load contract ABI and bytecode from the compiled contract
@pytest.fixture(scope='module')
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
        "nonce": nonce,
    })

    signed_tx = account.sign_transaction(tx)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction sent with hash: {web3.toHex(tx_hash)}")


# Test: Add candidates
# def test_add_candidates(web3, voting_contract):
#     tx1 = voting_contract.functions.addCandidates('Kirtan').build_transaction({
#         'from': web3.eth.default_account,
#         'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
#         'gas': 2000000,
#         'gasPrice': web3.to_wei('10', 'gwei')
#     })
#     send_transaction(web3, tx1, '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7')

#     tx2 = voting_contract.functions.addCandidates('Ram').build_transaction({
#         'from': web3.eth.default_account,
#         'nonce': web3.eth.get_transaction_count(web3.eth.default_account) + 1,
#         'gas': 2000000,
#         'gasPrice': web3.to_wei('10', 'gwei')
#     })
#     send_transaction(web3, tx2, '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7')

#     count = voting_contract.functions.candidatesCount().call()
#     assert count == 2, "Candidate count mismatch"

# # Test: Vote and get candidate
# def test_vote_and_get_candidate(web3, voting_contract):
#     tx = voting_contract.functions.vote(1).build_transaction({
#         'from': web3.eth.default_account,
#         'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
#         'gas': 2000000,
#         'gasPrice': web3.to_wei('10', 'gwei')
#     })
#     send_transaction(web3, tx, '0x64f7230c55ce366202d05591cf628050bee48da9aa4fed2ef5fa58c4a8c9e3a7')
#     candidate = voting_contract.functions.getCandidate(1).call()
#     assert candidate[2] == 1, "Vote count not updated correctly"

# # Test: Get total votes
# def test_get_totals(web3, voting_contract):
#     candidates_count, candidates_votes = voting_contract.functions.GetTotals().call()
#     assert candidates_count == 2, "Incorrect total candidates"
#     assert candidates_votes == 1, "Incorrect total votes"

# # Test: Get candidate votes
# def test_get_candidate_votes(web3, voting_contract):
#     candidate_votes = voting_contract.functions.GetCandidateVotes().call()
#     assert len(candidate_votes) == 2, "Incorrect count of candidates"
#     assert candidate_votes[0][2] == 1, "Incorrect count of votes for candidate 1"
#     assert candidate_votes[1][2] == 0, "Incorrect count of votes for candidate 2"