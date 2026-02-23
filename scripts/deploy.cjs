const { ethers } = require("hardhat");

async function main() {

  const [deployer] = await ethers.getSigners();

  console.log("Deploying with:", deployer.address);

  // ---- Deploy SupplyChain ----
  const SupplyChain = await ethers.getContractFactory("SupplyChain");

  // Constructor requires manufacturer address
  const supplyChain = await SupplyChain.deploy(deployer.address);
  await supplyChain.deployed();

  console.log("SupplyChain deployed to:", supplyChain.address);

  // ---- Deploy CryptoVerifier ----
  const CryptoVerifier = await ethers.getContractFactory("CryptoVerifier");

  const verifier = await CryptoVerifier.deploy();
  await verifier.deployed();

  console.log("CryptoVerifier deployed to:", verifier.address);

  // ---- Deploy HashTest ----
  const Lock = await ethers.getContractFactory("HashTest");

  const hashtest = await CryptoVerifier.deploy();
  await hashtest.deployed();

  console.log("hashtest deployed to:", hashtest.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
