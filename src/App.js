
import React, { useState } from "react";
import { ethers } from "ethers";
import vehiclesDB from "./vehiclesdb";
import TaxCongestionABI from "./TaxCongestionABI.json"; // Import ABI

const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // 🔁 Replace with deployed contract address






// // Simulated local "database"
// const vehicleDB = {
//   "3597AE-7": {
//     licensePlate: "3597AE-7",
//     owner: "Devika Kanyal",
//     model: "Honda bike",
//     type: "Private",
//   },
//   "UP32AA9999": {
//     licensePlate: "UP32AA9999",
//     owner: "Rohit Sharma",
//     model: "Suzuki Swift",
//     type: "Commercial",
//   },
//   "DL8CAF5032": {
//     licensePlate: "DL8CAF5032",
//     owner: "Anjali Verma",
//     model: "Hyundai i10",
//     type: "Private",
//   },
//   "HR26DK8337": {
//     licensePlate: "HR26DK8337",
//     owner: "Kunal Arora",
//     model: "Kia Seltos",
//     type: "Commercial",
//   },
// };

function App() {
  const [account, setAccount] = useState(null);
  const [plate, setPlate] = useState("");
  const [status, setStatus] = useState("");
  const [vehicleInfo, setVehicleInfo] = useState(null);
  const [taxAmount, setTaxAmount] = useState(null);
  const [userInfo, setUserInfo] = useState(null);



  // ✅ Hardcoded user info (mock data)
  const userDatabase = {
    "3597AE-7": {
      name: "John Doe",
      licensePlate: "3597AE-7",
    },
    "DL8CAF5032": {
      name: "Devika Kanyal",
      licensePlate: "DL8CAF5032",
    },
    // Add more if needed
  };

  // 🦊 Connect Wallet
  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });
        setAccount(accounts[0]);
      } catch (err) {
        console.error("Connection error:", err);
      }
    } else {
      alert("Please install MetaMask.");
    }
  };

  // 🚘 Register Vehicle to Smart Contract
  const registerVehicle = async () => {
    if (!account) return alert("Please connect wallet first.");
    if (!plate) return alert("Please enter a license plate.");
  
    const vehicleDetails = vehiclesDB[plate.toUpperCase()];
    if (!vehicleDetails) return alert("Vehicle not found in local database!");
  
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(CONTRACT_ADDRESS, TaxCongestionABI.abi, signer);
  
    try {
      const tx = await contract.registerVehicle(plate);
      await tx.wait();
  
      const data = await contract.getVehicle(plate);
      const parsedTax = ethers.utils.formatEther(data.taxAmount);
  
      setVehicleInfo(vehicleDetails);
      setTaxAmount(parsedTax);
      alert(`✅ Registered ${vehicleDetails.owner}'s vehicle (${plate}) successfully!`);
    } catch (error) {
      console.error(error);
      alert("❌ Registration failed or already registered.");
    }
  };

  const fetchVehicleDetails = () => {
    if (!plate) return alert("Please enter a license plate.");
  
    const normalizedPlate = plate.toUpperCase();
    const vehicleDetails = vehiclesDB[normalizedPlate];
    const userDetails = userDatabase[normalizedPlate];
  
    if (!vehicleDetails || !userDetails) {
      alert("❌ No matching user or vehicle found.");
      setVehicleInfo(null);
      setUserInfo(null);
      setTaxAmount(null);
      return;
    }
  
    setVehicleInfo(vehicleDetails);
    setUserInfo(userDetails);
  
    // Optionally reset any old tax info
    setTaxAmount(null);
  };
  

  const payTax = async () => {
    if (!account || !plate || !taxAmount) {
      alert("Missing information to pay tax.");
      return;
    }
  
    try {
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();
      const contract = new ethers.Contract(CONTRACT_ADDRESS, TaxCongestionABI.abi, signer);
  
      const tx = await contract.payTax(plate.toUpperCase(), {
        value: ethers.utils.parseEther(taxAmount.toString()),
      });
  
      await tx.wait();
      alert("✅ Tax paid successfully!");
    } catch (err) {
      console.error("Tax payment failed:", err);
      alert("❌ Tax payment failed. Check console or MetaMask.");
    }
  };
  
  

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🚦 Tax Congestion DApp</h2>

      {/* 🔗 Connect Wallet */}
      <button style={styles.button} onClick={connectWallet}>
        {account ? `✅ ${account.slice(0, 6)}... Connected` : "🔗 Connect Wallet"}
      </button>

      {/* 📝 Register Vehicle */}
      <div style={styles.formContainer}>
        <input
          style={styles.input}
          value={plate}
          onChange={(e) => setPlate(e.target.value)}
          placeholder="Enter License Plate (e.g., 3597AE-7)"
        />
        <button style={styles.registerButton} onClick={fetchVehicleDetails}>
          📝 show details
        </button>
      </div>

      {/* 📢 Status */}
      {status && <p style={{ marginTop: "20px" }}>{status}</p>}

      {vehicleInfo && (
      <div style={styles.vehicleCard}>
        <h3>Vehicle Info</h3>
        <p><strong>Owner:</strong> {vehicleInfo.owner}</p>
        <p><strong>Model:</strong> {vehicleInfo.model}</p>
        <p><strong>Type:</strong> {vehicleInfo.type}</p>
        <p><strong>License Plate:</strong> {vehicleInfo.licensePlate}</p>
        <p><strong>Tax to Pay:</strong> {vehicleInfo.taxAmount} ETH</p>
        <button style={styles.payButton} onClick={registerVehicle}>
          💰 Pay Tax 
        </button>
      </div>
)}


    </div>

    
  );
}

// 🎨 Styling
const styles = {
  container: {
    backgroundColor: "#121212",
    color: "#fff",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Arial, sans-serif",
    padding: "20px",
  },
  title: {
    fontSize: "28px",
    fontWeight: "bold",
    marginBottom: "20px",
  },
  button: {
    backgroundColor: "#1e88e5",
    color: "#fff",
    padding: "12px 18px",
    fontSize: "16px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginBottom: "20px",
    transition: "0.3s",
  },
  formContainer: {
    display: "flex",
    gap: "10px",
  },
  input: {
    padding: "12px",
    fontSize: "16px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    width: "250px",
  },
  registerButton: {
    backgroundColor: "#ff9800",
    color: "#fff",
    padding: "12px 18px",
    fontSize: "16px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    transition: "0.3s",
  },

  container: {
    backgroundColor: "#121212",
    backgroundImage: "url('/background.jpg')",
    backgroundSize: "cover",
    backgroundPosition: "center",
    color: "#fff",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Arial, sans-serif",
    padding: "20px",
  }
,  

  vehicleCard: {
    marginTop: "30px",
    backgroundColor: "#1e1e1e",
    padding: "20px",
    borderRadius: "10px",
    width: "300px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.3)",
    textAlign: "left"
  },
  payButton: {
    backgroundColor: "#4caf50",
    color: "#fff",
    padding: "10px 16px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    marginTop: "10px"
  }

  
};


export default App;
