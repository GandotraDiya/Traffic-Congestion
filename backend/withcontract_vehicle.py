from web3 import Web3
import json
import time

# Step 1: Connect to Hardhat local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.isConnected(), "Web3 connection failed"

# Step 2: Load ABI
with open('TaxCongestionABI.json', 'r') as file:
    abi = json.load(file)

# Step 3: Setup contract
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # 🔁 Replace with deployed contract address
contract = w3.eth.contract(address=contract_address, abi=abi)

# Step 4: Use first Hardhat account (unlocked by default)
account = w3.eth.accounts[0]

# Step 5: Input license plate
license_plate = "DL4CAF5039"

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
print(f"Tax Amount: {w3.fromWei(vehicle[2], 'ether')} ETH")
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
print(f"Tax Amount: {w3.fromWei(vehicle[2], 'ether')} ETH")
print(f"Registered: {vehicle[3]}")
print(f"Tax Paid: {vehicle[4]}")
