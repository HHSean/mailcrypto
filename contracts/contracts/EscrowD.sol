// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// imports
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Escrow is Ownable {
    // escrow contract, sends ether to a beneficiary address.
    // Sender needs to deposit with a password hash. Sender can withdraw anytime.
    // Receiver has to withdraw with the password hash.

    // struct transactions {
    //     address beneficiary;
    //     bytes32 passwordHash;
    //     uint256 amount;
    // }
    // mapping (uint => transactions) transactions;
    
    // // events
    // event Deposit(address indexed beneficiary, uint256 amount);
    // event Withdraw(address indexed beneficiary, uint256 amount);
    

    // // constructor
    // constructor() public {}    

    // // deposit ether to escrow.
    // function deposit(address _beneficiary, uint _amount, string memory _passwordHash) public {
    //     require(_amount > 0, "amount must be greater than 0");
    //     // require(_beneficiary != address(0), "beneficiary address cannot be 0");
    //     // require(_beneficiary != msg.sender, "beneficiary address cannot be sender");
    //     require(balanceOf(msg.sender) >= _amount, "sender does not have enough ether");

    //     beneficiaries[_beneficiary].beneficiary = _beneficiary;
    //     beneficiaries[_beneficiary].passwordHash = _passwordHash;
    //     beneficiaries[_beneficiary].amount = _amount;

    //     transfer(_beneficiary, _amount);
    //     emit Deposit(_beneficiary, _amount);
    // }

    // // withdraw ether from escrow.
    // function withdraw(string memory _passwordHash) public {
    //     require(beneficiaries[msg.sender].passwordHash == _passwordHash, "password hash does not match");
    // }
}
