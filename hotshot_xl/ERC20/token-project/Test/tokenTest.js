const { expect } = require("chai");
import { ethers } from "hardhat";

describe("KToken", function () {
    it("Should deploy and assign the correct initial supply", async function () {
        const [owner] = await ethers.getSigners();
        const Token = await ethers.getContractFactory("KToken");
        const token = await Token.deploy();

        await token.deployed();

        const totalSupply = await token.totalSupply();
        expect(totalSupply).to.equal(1000 * 10 ** 18);

        const balance = await token.balanceOf(owner.address);
        expect(balance).to.equal(1000 * 10 ** 18);
    });
});