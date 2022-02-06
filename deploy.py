from solcx import compile_standard
import json
from web3 import Web3

# open solidity file

with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# print compiled solidity to file
with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to web3
with open("./local_web3_data.json", "r") as file:
    local_web3_data = json.load(file)
    # print(local_web3_data)

web3 = Web3(Web3.HTTPProvider(local_web3_data["server"]))

# creating contract
simpleStorage_contract = web3.eth.contract(abi=abi, bytecode=bytecode)

chain_id = int(local_web3_data["network_id"])
address = local_web3_data["address"]
nonce = web3.eth.getTransactionCount(address)

simpleStorage_deploy_trx = simpleStorage_contract.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": nonce,
        "gasPrice": web3.eth.gas_price,
    }
)
simpleStorage_deploy_trx_signed = web3.eth.account.sign_transaction(
    simpleStorage_deploy_trx, local_web3_data["private_key"]
)
simpleStorage_deploy_trx_hash = web3.eth.send_raw_transaction(
    simpleStorage_deploy_trx_signed.rawTransaction
)
simpleStorage_deploy_trx_receipt = web3.eth.wait_for_transaction_receipt(
    simpleStorage_deploy_trx_hash
)
