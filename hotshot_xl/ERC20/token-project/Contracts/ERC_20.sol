// SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract KToken is ERC20 {
    constructor() ERC20("KToken", "KTK") {
        _mint(msg.sender, 1000 * 0 ** decimals());
    }
}