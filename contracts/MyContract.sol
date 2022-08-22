
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

    struct Person {
        uint256 age;
        string name;
    }
    struct FavoriteNumber {
        string name;
        uint256 number;
    }

contract MyContract {
    
    uint256 internal value; 
    Person internal dude;
    Person[] internal people;
    mapping(string => uint256) public nameToAge;

    constructor()  {
        value = 0;
    }

    function getPerson() public view returns(Person[] memory) {
        return people;
    }


    function setPerson(uint256 _age, string memory _name) public {
        // dude.age = _age;
        // dude.name = _name;

        // people.push(dude);
        people.push(Person(_age,_name));
        nameToAge[_name] = _age;
    }
}

contract Contract2 {
    MyContract _myContract;

    function createMyContract() public {
        _myContract = new MyContract();
    }

    function getPerson() view public returns(Person[] memory) {
        return _myContract.getPerson();
    }

    function setPerson(uint256 _age, string memory _name) public {
        _myContract.setPerson(_age, _name);
    }
}

contract Contract3 is Contract2 {}