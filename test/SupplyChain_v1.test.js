const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SupplyChain", function () {

  let supplyChain;
  let mockVerifier;
  let manufacturer;

  beforeEach(async function () {

    [manufacturer] = await ethers.getSigners();

    // Deploy Mock Verifier
    const MockVerifier = await ethers.getContractFactory("MockVerifier");
    mockVerifier = await MockVerifier.deploy();
    await mockVerifier.deployed();

    // Deploy SupplyChain with mock verifier
    const SupplyChain = await ethers.getContractFactory("SupplyChain");
    supplyChain = await SupplyChain.deploy(mockVerifier.address);
    await supplyChain.deployed();
  });

  it("Should register an item", async function () {

    const itemId = 1;
    const metadataHash = ethers.utils.formatBytes32String("test");

    const a = [1, 2];
    const b = [[1, 2], [3, 4]];
    const c = [1, 2];
    const publicSignals = [5, 6];

    await supplyChain.registerItem(
      itemId,
      metadataHash,
      a,
      b,
      c,
      publicSignals
    );

    const item = await supplyChain.items(itemId);

    expect(item.exists).to.equal(true);
    expect(item.manufacturer).to.equal(manufacturer.address);
  });

});
