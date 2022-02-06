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

