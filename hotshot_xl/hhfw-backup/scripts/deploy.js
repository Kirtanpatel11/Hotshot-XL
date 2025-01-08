// Import Hardhat
const hre = require("hardhat");

async function main() {
    // Get the deployer account
    const [deployer] = await hre.ethers.getSigners();

    console.log("Deploying contracts with the account:", deployer.address);

    // Get the contract factory and deploy the contract
    const Token = await hre.ethers.getContractFactory("Token");
    const token = await Token.deploy();

    // Wait for the deployment to complete
    await token.deployed();

    console.log("Token deployed to:", token.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });

    