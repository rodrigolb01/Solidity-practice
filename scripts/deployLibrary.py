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

#for connecting to Ganache (localhost blockchain)
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545")) 
#for connecting to Goerli (testnet)
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/141d722c9b834dc9a38a0bf0dd40cfe8"))

#for Ganache
# chain_id = 1337
#for Goerli
chain_id = 5
#for Ganache
# my_address = '0x29169dc8Bc228decFe54063C000f5CDf64953eD7'
#for Goerli
my_address = '0x44818e00A3E71582858425707746fb7DDFab927e'
private_key =  os.getenv("GOERLI_PRIVATE_KEY")

#create the contract in Python
Library = w3.eth.contract(abi=abi, bytecode=bytecode)
print(Library)
#get the latest transaction
nonce = w3.eth.getTransactionCount(my_address) # if 0 is because the address hasn't been used yet
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
#sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#send transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#wait for block confirmation to happen
print('generated receipt:')
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#Interacting with the contract
library = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(library.functions.listBooks().call())
#Calls don't make a state change
#Transacts make changes in the state
addBook_tx = library.functions.addBook('Trip to the center of the Earth',1).buildTransaction(
     {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1
    }
)
print(addBook_tx)
#sign
signed_addBook_txn = w3.eth.account.sign_transaction(addBook_tx, private_key=private_key)
#send contract (DEPLOYING)
print("Deploying")
addBook_tx_hash = w3.eth.send_raw_transaction(signed_addBook_txn.rawTransaction)
#waiting confirmation
tx_addBook_receipt = w3.eth.wait_for_transaction_receipt(addBook_tx_hash)
print(library.functions.listBooks().call())

