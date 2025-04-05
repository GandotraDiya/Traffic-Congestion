import cv2
import pytesseract
import os
import json
from web3 import Web3

# --- OCR Setup ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\91708\tesseract.exe"

# --- Web3 Setup ---
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Update if you're using Infura

# Load contract ABI
with open("backend/contracts/TaxCongestionABI.json") as f:
    abi = json.load(f)

# Contract setup
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract = w3.eth.contract(address=contract_address, abi=abi)

# Your wallet
account = "0x2B2fDCc16F6Cb4FC3f7B3a689CE8b8FFCD69A762"
private_key = "679098e68bd86eb6f13b4a1cfa233d3f84e0fbda9405a3ba65fd5c20fb3a77f1"

# --- Video Capture Setup ---
cap = cv2.VideoCapture(1)  # Iriun cam
if not os.path.exists("captured_frames"):
    os.makedirs("captured_frames")

frame_count = 0
seen_plates = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame")
        break

    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # OCR
    text = pytesseract.image_to_string(gray, config='--psm 8')
    plate = text.strip().replace(" ", "").replace("\n", "")
    
    # Display and Save
    frame_path = f"captured_frames/frame_{frame_count}.jpg"
    cv2.imwrite(frame_path, frame)
    print(f"✅ Saved frame: {frame_path}")
    frame_count += 1
    cv2.imshow("Live Feed - Press 'q' to Exit", frame)

    # 🔁 If plate looks valid and hasn't been seen
    if len(plate) >= 6 and plate not in seen_plates:
        print(f"🎯 License Plate Detected: {plate}")
        seen_plates.add(plate)

        try:
            # Send to blockchain
            nonce = w3.eth.get_transaction_count(account)
            tx = contract.functions.registerVehicle(plate).build_transaction({
                "from": account,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": w3.to_wei("20", "gwei")
            })

            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            print(f"✅ Vehicle '{plate}' registered on blockchain.\n🔗 Tx Hash: {tx_hash.hex()}")

        except Exception as e:
            print(f"❌ Blockchain error: {e}")

    # Exit on q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
