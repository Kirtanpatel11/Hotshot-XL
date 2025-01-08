require("@nomiclabs/hardhat-ethers");
require("dotenv").config();

module.exports = {
  solidity: "0.8.20",
  networks: {
    bscTestnet: {
      url: process.env.BSC_TESTNET_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};