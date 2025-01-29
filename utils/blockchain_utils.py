from eth_account import Account
from solders.keypair import Keypair
from base58 import b58encode

def generate_ethereum_address():
    account = Account.create()
    return {
        "address": account.address,
        "private_key": account.key.hex()
    }

def generate_solana_address():
    keypair = Keypair.generate()
    return {
        "address": b58encode(keypair.public_key).decode(),
        "private_key": b58encode(keypair.secret_key).decode()
    }