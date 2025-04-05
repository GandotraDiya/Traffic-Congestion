import { ethers } from "ethers";
import TaxCongestionABI from "./TaxCongestionABI.json";

// Replace with your deployed contract address
const CONTRACT_ADDRESS = "0xYourContractAddress";

export const getContract = async () => {
  if (window.ethereum) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(CONTRACT_ADDRESS, TaxCongestionABI, signer);
    return contract;
  } else {
    alert("Please install MetaMask");
  }
};
