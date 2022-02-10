from web3 import Web3
import json


# get local network data
with open("./local_web3_data.json") as file:
    local_web3_data = json.load(file)

# init connection
web3 = Web3(Web3.HTTPProvider(local_web3_data["server"]))
print(web3.isConnected())
