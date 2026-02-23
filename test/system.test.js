const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SupplyChain + CryptoVerifier", function () {

    let manufacturer, user;
    let supplyChain, verifier;

    beforeEach(async function () {

        [manufacturer, user] = await ethers.getSigners();

        // Deploy SupplyChain (NO constructor args)
        const SupplyChain = await ethers.getContractFactory("SupplyChain");
        supplyChain = await SupplyChain.deploy(manufacturer.address);
        await supplyChain.deployed();


        // Deploy CryptoVerifier
        const CryptoVerifier = await ethers.getContractFactory("CryptoVerifier");
        verifier = await CryptoVerifier.deploy();
        await verifier.deployed();
    });

    // Helper: generate commitment same as your JS script
    function generateCommitment() {

        const a = [123, 456];
        const b = [
            [789, 111],
            [222, 333]
        ];

        const packed1 = ethers.utils.solidityPack(
            ["uint256", "uint256", "uint256", "uint256", "uint256", "uint256"],
            [a[0], a[1], b[0][0], b[0][1], b[1][0], b[1][1]]
        );
        const hash1 = ethers.utils.keccak256(packed1);

        const packed2 = ethers.utils.solidityPack(
            ["uint256", "uint256", "uint256"],
            [hash1, b[1][0], b[0][0]]
        );
        const hash2 = ethers.utils.keccak256(packed2);

        const packed3 = ethers.utils.solidityPack(
            ["uint256", "uint256"],
            [hash2, a[1]]
        );
        return ethers.utils.keccak256(packed3);
    }

    it("Should register an item with valid signature", async function () {

        const itemId = 1;
        const commitment = generateCommitment();

        // Manufacturer signs commitment
        const signature = await manufacturer.signMessage(
            ethers.utils.arrayify(commitment)
        );

        const sig = ethers.utils.splitSignature(signature);

        await supplyChain.connect(manufacturer).registerItem(
            itemId,
            commitment,
            sig.v,
            sig.r,
            sig.s
        );

        const item = await supplyChain.getItem(itemId);

        expect(item[0]).to.equal(manufacturer.address);
        expect(item[1]).to.equal(commitment);
    });

    it("Should fail if non-manufacturer tries to register", async function () {

        const itemId = 2;
        const commitment = generateCommitment();

        const signature = await manufacturer.signMessage(
            ethers.utils.arrayify(commitment)
        );

        const sig = ethers.utils.splitSignature(signature);

        await expect(
            supplyChain.connect(user).registerItem(
                itemId,
                commitment,
                sig.v,
                sig.r,
                sig.s
            )
        ).to.be.revertedWith("Not authorized");
    });


    it("CryptoVerifier should validate correct signature", async function () {

        const commitment = generateCommitment();

        const signature = await manufacturer.signMessage(
            ethers.utils.arrayify(commitment)
        );

        const sig = ethers.utils.splitSignature(signature);

        const result = await verifier.verifyCommitment(
            commitment,
            manufacturer.address,
            sig.v,
            sig.r,
            sig.s
        );

        expect(result).to.equal(true);
    });

    it("CryptoVerifier should fail for wrong signer", async function () {

        const commitment = generateCommitment();

        const signature = await user.signMessage(
            ethers.utils.arrayify(commitment)
        );

        const sig = ethers.utils.splitSignature(signature);

        const result = await verifier.verifyCommitment(
            commitment,
            manufacturer.address,
            sig.v,
            sig.r,
            sig.s
        );

        expect(result).to.equal(false);
    });

});
