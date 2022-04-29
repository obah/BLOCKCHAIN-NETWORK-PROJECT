import pytest

from Backend.Blockchain.BLOCKCHAIN import Blockchain
from Backend.Wallet.transaction import Transaction
from Backend.Wallet.wallet import Wallet
from Backend.Blockchain.BLOCK import GENESIS_DATA

#we test the blockchain instance first
def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain_five_blocks():
    blockchain = Blockchain()
    for i in range (5):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain

def test_is_valid_chain(blockchain_five_blocks):
    Blockchain.is_valid_chain(blockchain_five_blocks.chain)

def test_is_valid_chain_bad_genesis(blockchain_five_blocks):
    blockchain_five_blocks.chain[0].hash = 'foobar-hash'

    with pytest.raises(Exception, match = 'genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain_five_blocks.chain)

def test_replace_chain(blockchain_five_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_five_blocks.chain)

    assert blockchain.chain == blockchain_five_blocks.chain

def test_replace_chain_not_longer(blockchain_five_blocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match = 'the incoming chain must be longer'):
        blockchain_five_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(blockchain_five_blocks):
    blockchain = Blockchain()
    blockchain_five_blocks.chain[1].hash = 'evil-hashes, hahaha!'

    with pytest.raises(Exception, match = 'the incoming chain is invalid'):
        blockchain.replace_chain(blockchain_five_blocks.chain)

def test_valid_transaction_chain(blockchain_five_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_five_blocks.chain)

def test_valid_transaction_chain_duplicate_transactions(blockchain_five_blocks):
    transaction = Transaction(Wallet(), 'recipient', 1).to_json()
    blockchain_five_blocks.add_block([transaction, transaction])

    with pytest.raises(Exception, match='is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_five_blocks.chain)

def test_valid_transaction_chain_multiple_rewards(blockchain_five_blocks):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()
    blockchain_five_blocks.add_block([reward_1, reward_2])

    with pytest.raises(Exception, match='one mining reward per block'):
        Blockchain.is_valid_transaction_chain(blockchain_five_blocks.chain)

def test_valid_transaction_chain_bad_transaction(blockchain_five_blocks):
    bad_transaction = Transaction(Wallet(), 'recipient', 10)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_five_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_five_blocks.chain)

def test_valid_transaction_chain_bad_historic_balance(blockchain_five_blocks):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, 'recipient', 30)
    bad_transaction.output[wallet.address] = 9001
    bad_transaction.input['amount'] = 9031
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

    blockchain_five_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception, match='has an invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain_five_blocks.chain)