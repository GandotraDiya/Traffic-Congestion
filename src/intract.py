from web3 import Web3
import json
import time

# Step 1: Connect to Hardhat local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected(), "Web3 connection failed"

# Step 2: Load ABI
# with open('TaxCongestionABI.json', 'r') as file:
#     abi = json.load(file)["abi"]

abi=[
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "licensePlate",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "payer",
          "type": "address"
        }
      ],
      "name": "TaxPaid",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "licensePlate",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "entryTimestamp",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "taxAmount",
          "type": "uint256"
        }
      ],
      "name": "VehicleRegistered",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_licensePlate",
          "type": "string"
        }
      ],
      "name": "getVehicle",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "licensePlate",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "entryTimestamp",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "taxAmount",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "isRegistered",
              "type": "bool"
            },
            {
              "internalType": "bool",
              "name": "isTaxPaid",
              "type": "bool"
            }
          ],
          "internalType": "struct TaxCongestion.Vehicle",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_licensePlate",
          "type": "string"
        }
      ],
      "name": "payTax",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_licensePlate",
          "type": "string"
        }
      ],
      "name": "registerVehicle",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "vehicles",
      "outputs": [
        {
          "internalType": "string",
          "name": "licensePlate",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "entryTimestamp",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "taxAmount",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isRegistered",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "isTaxPaid",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "withdraw",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]

# Step 3: Setup contract
contract_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"  # 🔁 Replace with deployed contract address
contract = w3.eth.contract(address=contract_address, abi=abi)

# Step 4: Use first Hardhat account (unlocked by default)
account = w3.eth.accounts[0]

# Step 5: Input license plate
license_plate = f"3579EA-7_{int(time.time())}"  # adds timestamp for uniqueness


# --- Register Vehicle ---
print("Registering vehicle...")
tx_register = contract.functions.registerVehicle(license_plate).transact({
    'from': account
})
w3.eth.wait_for_transaction_receipt(tx_register)

# --- Get Vehicle Data ---
vehicle = contract.functions.getVehicle(license_plate).call()
print("Vehicle Data After Registration:")
print(f"License: {vehicle[0]}")
print(f"Timestamp: {vehicle[1]}")
print(f"Tax Amount: {w3.from_wei(vehicle[2], 'ether')} ETH")
print(f"Registered: {vehicle[3]}")
print(f"Tax Paid: {vehicle[4]}")

# --- Pay Tax ---
print("Paying tax...")
tx_pay = contract.functions.payTax(license_plate).transact({
    'from': account,
    'value': vehicle[2]  # taxAmount in wei
})
w3.eth.wait_for_transaction_receipt(tx_pay)

# --- Get Vehicle Data Again ---
vehicle = contract.functions.getVehicle(license_plate).call()
print("\nVehicle Data After Tax Payment:")
print(f"License: {vehicle[0]}")
print(f"Timestamp: {vehicle[1]}")
print(f"Tax Amount: {w3.from_wei(vehicle[2], 'ether')} ETH")
print(f"Registered: {vehicle[3]}")
print(f"Tax Paid: {vehicle[4]}")
