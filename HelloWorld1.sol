// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;

contract Mycontract{
  struct User {
        address userAddress;
        uint256 balance;
  }

  mapping(address => User) public usersInfo;

  event AddBalance(address indexed userAddress, uint256 amount);

  function deposit() public payable {
    require(msg.value > 0, "Amount < 0");

    User storage user = usersInfo[msg.sender];
    if (user.userAddress == address(0)) {
        user.userAddress = msg.sender;
    }
    user.balance += msg.value;

    emit AddBalance(msg.sender, msg.value);
  }

  function getBalance(address user) public view returns (uint256) {
        return usersInfo[user].balance;
  }

  function withdraw(uint256 amount) public payable{
        require(amount > 0, "Amount < 0");
        require(usersInfo[msg.sender].balance >= amount, "Incorrect balance");

        payable(msg.sender).transfer(amount);
        usersInfo[msg.sender].balance -= amount;
        
  } 
}
      