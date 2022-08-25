import os
from solcx import compile_standard, install_solc;
import json;
from web3 import Web3;
from dotenv import load_dotenv
install_solc("0.6.0")

load_dotenv()

with open("D:\Leassons and Assignments\Solidity practice\contracts\Library.sol", "r") as file:
    library_file = file.read()

#Compile our Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Library.sol" : {"content": library_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["Library.sol"]["Library"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["Library.sol"]["Library"]["abi"]

#for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = '0x8fF85A45039c25708e37B2CBe29fb6e90fFE11aE'
#DON'T DO THIS! #DON'T DO THIS! #DON'T DO THIS!
private_key =  os.getenv("PRIVATE_KEY")

#create the contract in Python
Library = w3.eth.contract(abi=abi, bytecode=bytecode)
print(Library)
#get the latestest transaction
nonce = w3.eth.getTransactionCount(my_address) #0 because the address hasn't been used yet
#build a transaction
transaction = Library.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    }
)
print(transaction)
#sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
