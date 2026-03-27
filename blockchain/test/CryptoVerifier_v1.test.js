const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CryptoVerifier", function () {
  it("Should verify signature", async function () {

    const Verifier = await ethers.getContractFactory("CryptoVerifier");
    const verifier = await Verifier.deploy();
    await verifier.deployed();

    const [manufacturer] = await ethers.getSigners();

    const productId = "P123";
    const timestamp = 123456;

    const messageHash = ethers.utils.keccak256(
      ethers.utils.solidityPack(
        ["string", "address", "uint256"],
        [productId, manufacturer.address, timestamp]
      )
    );

    const signature = await manufacturer.signMessage(
      ethers.utils.arrayify(messageHash)
    );

    const sig = ethers.utils.splitSignature(signature);

    const result = await verifier.verify(
      productId,
      manufacturer.address,
      timestamp,
      sig.v,
      sig.r,
      sig.s
    );

    expect(result).to.equal(true);
  });
});
