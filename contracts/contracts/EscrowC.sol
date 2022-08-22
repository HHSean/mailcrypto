// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// imports
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⣶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡀⢻⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀
// ⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠷⠆⠀⠀
// ⠀⠀⠀⣼⣿⣿⡿⠟⠛⠉⣉⣀⠘⣿⣿⣿⡿⠿⠿⠟⠛⠛⠉⣉⣀⣤⣤⣶⠂⠀
// ⠀⠀⣼⠟⠉⣀⣤⣶⣿⣿⣿⣿⣦⣤⣤⣤⡀⢠⣶⣶⣾⣿⣿⣿⣿⣿⣿⠃⠀⠀
// ⠀⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⢿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀
// ⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠸⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⠿⣿⣿⡇⢻⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀
// ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

contract EscrowC is Ownable {
    // escrow contract, sends ether to a beneficiary address.
    // beta version of the decentralized escrow contract.
    // This is still centralized (relies on Oracle). Decentralized is possible,
    // but need to figure out a few kinks with gas costs and frontrunning.

    struct transaction {
        address sender;
        string recipient; // email
        uint256 amount; // amount to send
    }
    transaction[] transactions; // array of transactions
    mapping(string => address) emails; // mapping of email to address

    // events
    event Deposit(
        address indexed sender,
        string indexed recipient,
        uint256 amount
    );
    event Withdraw(address indexed recipient, uint256 amount);

    // constructor
    constructor() {}

    // deposit ether to escrow.
    function deposit(string calldata _recipient) external payable {
        require(msg.value > 0, "deposit must be greater than 0");

        // if recipient email address already has a crypto address, send directly
        if (emails[_recipient] != address(0)) {
            // transfer ether directly to recipient
            payable(emails[_recipient]).transfer(msg.value);
            emit Deposit(msg.sender, _recipient, msg.value);
        } else {
            // store new transaction
            transaction memory newTransaction;
            newTransaction.recipient = _recipient;
            newTransaction.amount = msg.value;
            newTransaction.sender = msg.sender;
            transactions.push(newTransaction);
            emit Deposit(msg.sender, _recipient, msg.value);
        }
    }

    // sender can withdraw deposited ether from a transaction
    function withdrawSender(uint256 _index) external {
        require(_index < transactions.length, "index out of bounds");
        require(
            transactions[_index].sender == msg.sender,
            "only sender can withdraw"
        );

        // transfer ether back to sender
        payable(msg.sender).transfer(transactions[_index].amount);
        emit Withdraw(transactions[_index].sender, transactions[_index].amount);

        // remove transaction from array
        delete transactions[_index];
    }

    // centralized transfer function to transfer ether to recipients newly created wallet
    function withdrawOwner(uint256 _index, address _recipient)
        external
        onlyOwner
    {
        require(_index < transactions.length, "index out of bounds");

        // transfer ether to recipient
        payable(_recipient).transfer(transactions[_index].amount);
        emit Withdraw(_recipient, transactions[_index].amount);

        // remove transaction from array
        delete transactions[_index];
    }

    //// Some utility functions ////

    function getAddress(string calldata _email)
        external
        view
        returns (address)
    {
        return emails[_email];
    }

    function getTransaction(uint256 _index)
        external
        view
        returns (transaction memory)
    {
        return transactions[_index];
    }

    function getTransactionCount() external view returns (uint256) {
        return transactions.length;
    }

    function getTransactionCountSent(address _sender)
        external
        view
        returns (uint256)
    {
        uint256 count = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].sender == _sender) {
                count++;
            }
        }
        return count;
    }

    function compareStrings(string memory _a, string memory _b)
        public
        view
        returns (bool)
    {
        return
            keccak256(abi.encodePacked(_a)) == keccak256(abi.encodePacked(_b));
    }

    function getTransactionCountReceived(string memory _email)
        external
        view
        returns (uint256)
    {
        uint256 count = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (compareStrings(transactions[i].recipient, _email)) {
                count++;
            }
        }
        return count;
    }

    // and that's all!
}
