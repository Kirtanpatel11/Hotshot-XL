require("@nomiclabs/hardhat-waffle");

module.exports = {
  solidity: "0.8.20",
  networks: {
    ganache: {
      url: "http://127.0.0.1:7545", // Ganache default URL
      accounts: [
        "0xae26f4b0ba5b1cf1aa0c40246571615ddd41b8e618163e2927eadfd608448d1c",
        "0x28582f21954b563d4d21ddf73989c3d4062f5e06ed1623f17dfa06c69844e8f6", // Replace with your Ganache account private keys
        "0x06bfe707e20d0695657643bd7b7fbfcc613fb91f46145a02a3ff7e2dcb5f911a",
        "0x4fb91ac878d6a01f6f6c62c38e4ac4b34e32b22b34c52b0bd3ba82e3df8e6c18", // You can add more keys if needed
        "0xfcb55ea58b490a282273894f2e302eba2ad698af6856f533be221464f39a1d28"
      ]
    }
  }
}