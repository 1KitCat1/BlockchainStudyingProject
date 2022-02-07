from solcx import compile_standard
import json
from web3 import Web3

# open solidity file
print("Getting contract code")
with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# compile solidity
print("Compiling contract")
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
print("Getting web3 connection data")
with open("./local_web3_data.json", "r") as file:
    local_web3_data = json.load(file)
    # print(local_web3_data)

web3 = Web3(Web3.HTTPProvider(local_web3_data["server"]))
print("Connected to web3")
# creating contract
simpleStorage_contract_creating = web3.eth.contract(abi=abi, bytecode=bytecode)

chain_id = int(local_web3_data["network_id"])
address = local_web3_data["address"]
nonce = web3.eth.getTransactionCount(address)

print("Creating contract transation")
simpleStorage_deploy_trx = (
    simpleStorage_contract_creating.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "from": address,
            "nonce": nonce,
            "gasPrice": web3.eth.gas_price,
        }
    )
)
print("Signing creating contract transation")
simpleStorage_deploy_trx_signed = web3.eth.account.sign_transaction(
    simpleStorage_deploy_trx, local_web3_data["private_key"]
)
print("Sending creating contract transaction")
simpleStorage_deploy_trx_hash = web3.eth.send_raw_transaction(
    simpleStorage_deploy_trx_signed.rawTransaction
)
simpleStorage_deploy_trx_receipt = web3.eth.wait_for_transaction_receipt(
    simpleStorage_deploy_trx_hash
)
print("Contract deployed\n")

# working with contract
print("Getting contract from web3")
simpleStorage_contract = web3.eth.contract(
    address=simpleStorage_deploy_trx_receipt.contractAddress, abi=abi
)
print("Creating store transaction")
store_transaction = simpleStorage_contract.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": web3.eth.getTransactionCount(address),
        "gasPrice": web3.eth.gas_price,
    }
)
store_transaction_signed = web3.eth.account.sign_transaction(
    store_transaction, private_key=local_web3_data["private_key"]
)
store_transaction_hash = web3.eth.send_raw_transaction(
    store_transaction_signed.rawTransaction
)
print("Transaction has been sended")
print("Getting stored number: ")
print(simpleStorage_contract.functions.retrive().call())
