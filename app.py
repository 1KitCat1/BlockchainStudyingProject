from web3 import Web3
import json


# get local network data
with open("./local_web3_data.json") as file:
    local_web3_data = json.load(file)

# init connection
web3 = Web3(Web3.HTTPProvider(local_web3_data["server"]))
if web3.isConnected():
    print("Connection established successfully")
else :
    print("Unable to establish connection!")

# get transaction data

address_from = local_web3_data["address"]
address_to = local_web3_data["address2"]

trx = {
    'nonce' : web3.eth.getTransactionCount(address_from),
    'to' : address_to,
    'value' : web3.toWei(1, 'ether'),
    'gas' : 100_000,
    'gasPrice' : web3.toWei(50, 'gwei')
}

signed_trx = web3.eth.account.sign_transaction(trx, local_web3_data["private_key"])
trx_hash = web3.eth.send_raw_transaction(signed_trx.rawTransaction)
print(web3.toHex(trx_hash))