import json
import web3
from web3.middleware import geth_poa_middleware
import os
import dotenv
dotenv.load_dotenv("../.env")

CONTRACT_ADDRESS = "0xEb5AE49BB91709Bd8Be77924854DF093c2C5Ce8f"
NETWORK = "mumbai"
PROVIDER_URL = os.getenv("INFURA_POLYGON_MUMBAI_URI")
ADMIN_ACCOUNT_KEY = os.getenv("PRIVATE_KEY")

# load abi from abi.json
with open("abi.json") as f:
    abi = json.load(f)

# create web3 instance
web3 = web3.Web3(web3.Web3.HTTPProvider(PROVIDER_URL))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.eth.defaultAccount = web3.eth.account.privateKeyToAccount(ADMIN_ACCOUNT_KEY).address

# create contract instance
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# create admin account
admin_account = web3.eth.account.privateKeyToAccount(ADMIN_ACCOUNT_KEY)


def make_deposit(recipient, amount):
    print(f"Contract Balance: {get_balance(CONTRACT_ADDRESS)}. Deposit Amount: {amount}")
    
    # create and sign transaction
    txn = contract.functions.deposit(recipient).buildTransaction({
        'value': amount,
        'gas': 100000,
        "nonce": web3.eth.getTransactionCount(web3.eth.defaultAccount),
    })
    signed_txn = admin_account.signTransaction(txn)

    # send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Transaction hash: {web3.toHex(tx_receipt.transactionHash)}")
    print(f"Contract Balance: {get_balance(CONTRACT_ADDRESS)}")
    return tx_receipt


def make_withdrawal(index, recipient):
    # makes an ether withdrawal to the recipient if the key is correct
    print(f"Contract Balance: {get_balance(CONTRACT_ADDRESS)}. Withdrawing deposit {index} to {recipient}")

    # 1. call contract withdrawOwner
    txn = contract.functions.withdrawOwner(index, recipient).buildTransaction({
        'gas': 100000,
        "nonce": web3.eth.getTransactionCount(web3.eth.defaultAccount),
    })
    signed_txn = admin_account.signTransaction(txn)

    # 2. send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)    
    print(f"Transaction hash: {web3.toHex(tx_receipt.transactionHash)}")
    print(f"Contract Balance: {get_balance(CONTRACT_ADDRESS)}")
    return tx_receipt



def get_balance(address):
    return web3.eth.getBalance(address)


if __name__ == "__main__":
    # send test deposit of 0.33 MATIC
    # make_deposit("test@hugomontenegro.com", web3.toWei(0.33, "ether"))

    # make withdrawal
    make_withdrawal(0, web3.eth.defaultAccount)





#     # now we mint the nft with contract.mint(token_uri, to)
#     contract_address = "0x0A1E0dfdcF8763415BC9c112B999A00bAbd1b491"
#     with open("abi.json") as f:
#         contract_abi = json.load(f)
#     to_address = "0x6B3751c5b04Aa818EA90115AA06a4D9A36A16f02"
#     PRIVATE_KEY = os.getenv("PRIVATE_KEY")
#     INFURA_ID = os.getenv("WEB3_INFURA_PROJECT_ID")
#     INFURA_URL = f"https://rinkeby.infura.io/v3/{INFURA_ID}"
#     web3 = Web3(HTTPProvider(INFURA_URL))
#     web3.middleware_onion.inject(geth_poa_middleware, layer=0)
#     web3.eth.defaultAccount = web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address
#     contract = web3.eth.contract(address=contract_address, abi=contract_abi)

#     # create and sign transaction
#     txn = contract.functions.mint(metadata_cid, to_address).buildTransaction(
#         {
#             "nonce": web3.eth.getTransactionCount(web3.eth.defaultAccount),
#             "gas": 1000000,
#             "gasPrice": web3.toWei("2", "gwei"),
#             "value": 0,
#         }
#     )
#     signed_txn = web3.eth.account.signTransaction(txn, PRIVATE_KEY)
#     tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
#     tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
#     token_id = tx_receipt.logs[0]["topics"][3]

#     # decode
#     token_id = web3.toInt(token_id)
#     tx_hash = web3.toHex(tx_hash)
#     return tx_hash, token_id, img_uri, sound_uri