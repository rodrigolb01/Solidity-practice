import os
from solcx import compile_standard, install_solc;
import json;
from web3 import Web3;
from dotenv import load_dotenv

install_solc("0.6.0")
load_dotenv()

with open("D:\Leassons and Assignments\Solidity practice\contracts\FundMe.sol", "r") as file:
    FundMe_file = file.read()

#Compile our Soldity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"FundMe.sol" : {"content": FundMe_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}

            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_sol", "w") as file:
    json.dump(compiled_sol)

#get bytecode
bytecode = compiled_sol["contracts"]["FundMe.sol"]["FundMe"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["FundMe.sol"]["FundMe"]["abi"]

#for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = '0x29169dc8Bc228decFe54063C000f5CDf64953eD7'
private_key =  os.getenv("PRIVATE_KEY")

#create the contract in Python
FundMe = w3.eth.contract(abi=abi, bytecode=bytecode)
print(FundMe)
#get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
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
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
#send transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#wait for block confirmation to happen
print('generated receipt:')
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#Interact with the contract

