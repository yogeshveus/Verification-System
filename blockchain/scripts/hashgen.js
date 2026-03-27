const { ethers } = require("hardhat");

async function main() {

  const [wallet] = await ethers.getSigners();

  const a = [123, 456];
  const b = [
    [789, 111],
    [222, 333]
  ];

  // hash1
  const packed1 = ethers.utils.solidityPack(
    ["uint256","uint256","uint256","uint256","uint256","uint256"],
    [a[0], a[1], b[0][0], b[0][1], b[1][0], b[1][1]]
  );
  const hash1 = ethers.utils.keccak256(packed1);

  // hash2
  const packed2 = ethers.utils.solidityPack(
    ["uint256","uint256","uint256"],
    [hash1, b[1][0], b[0][0]]
  );
  const hash2 = ethers.utils.keccak256(packed2);

  // hash3
  const packed3 = ethers.utils.solidityPack(
    ["uint256","uint256"],
    [hash2, a[1]]
  );
  const hash3 = ethers.utils.keccak256(packed3);

  const signature = await wallet.signMessage(
    ethers.utils.arrayify(hash3)
  );

  console.log("Commitment (hash3):", hash3);
  console.log("Signature:", signature);
}

main().catch(console.error);
