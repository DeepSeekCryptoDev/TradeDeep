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
    keypair = Keypair()
    return {
        "address": b58encode(bytes(keypair.pubkey())).decode(),
        "private_key": b58encode(keypair.secret() + bytes(keypair.pubkey())).decode()
    }