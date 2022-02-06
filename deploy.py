from solcx import compile_standard
import json
from web3 import Web3
# open solidity file
with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# install_solc("0.6.0")
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
abi = compiled_sol["contrants"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
