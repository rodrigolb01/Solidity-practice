// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "./Library.sol";

contract LibraryManager {

    Library[] public libraryArray;

    function createLibrary() public {
        Library lib = new Library();
        libraryArray.push(lib);
    }

    function sfStoreInLibrary(uint256 _libraryId, uint256 _bookId, string memory _bookTitle) public 
    {
        Library(address(libraryArray[_libraryId])).addBook(_bookTitle, _bookId);
    }

    function sfGetFromLibrary(uint256 _libraryId, uint256 _bookId) public view returns(string memory)
    {
        return Library(address(libraryArray[_libraryId])).bookByIdentifier(_bookId);
    }
}