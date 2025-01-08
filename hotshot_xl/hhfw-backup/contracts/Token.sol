// SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.20;

import "hardhat/console.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Token is Pausable, Ownable{
    string public name = "HardHat Token";
    string public symbol = "HHT";
    uint256 public totalSupply = 10000;

    address public owner;

    mapping(address => uint256) balances;

    constructor() {
        balances[msg.sender] = totalSupply;
        transferOwnership(msg.sender);
    }

    function transfer(address to, uint256 amount) external {
        console.log("**Sender balance is %s tokens**",balances[msg.sender]);
        console.log(
            "**Sender is sending %s tokens to %s address**",
            amount,
            to
        );

        require(balances[msg.sender] >= amount, "Not enough tokens");
        balances[msg.sender]-= amount;
        balances[to] += amount;
    }

    function balanceOf(address account) external view returns(uint256){
        return balances[account];
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();  
    }
}