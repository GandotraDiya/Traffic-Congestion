const hre = require("hardhat");

async function main() {
  const TaxCongestion = await hre.ethers.getContractFactory("TaxCongestion");
  const taxCongestion = await TaxCongestion.deploy();

  await taxCongestion.waitForDeployment(); // NEW: use this instead of .deployed()
  console.log("Contract deployed to:", await taxCongestion.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
