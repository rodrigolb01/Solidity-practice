from solcx import compile_standard, install_solc;
import json;

install_solc("0.6.0")

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
