// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;
pragma experimental ABIEncoderV2;

struct Book {
        string title;
        uint256 identifier;
    }
    

contract Library {
   
    Book[] array;
    mapping(uint256 => string) public bookByIdentifier;

    function addBook(string memory _title, uint256 _identifier) public {
        require(bytes(bookByIdentifier[_identifier]).length == 0, "repeated entry not allowed");
        array.push(Book(_title, _identifier));
        bookByIdentifier[_identifier] = _title;
    }

    function listBooks() public view returns(Book[] memory)
    {
        return array;
    }
}