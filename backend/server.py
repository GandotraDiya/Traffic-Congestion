from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# hardcoded vehicle info
vehicle_info = {
    "3597AE-7": {
        "licensePlate": "3597AE-7",
    }
}

@app.route("/send-to-blockchain", methods=["POST"])
def send_to_blockchain():
    data = request.get_json()
    number_plate = data.get("plate")

    vehicle = vehicle_info.get(number_plate)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    # Call your frontend or a script to register the vehicle on blockchain
    requests.post("http://localhost:3000/register", json=vehicle)

    return jsonify({"message": "Data sent to blockchain"})

if __name__ == "__main__":
    app.run(port=5000)
