// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TaxCongestion 
    {
    
    struct Vehicle {
        string licensePlate;
        uint256 entryTimestamp;
        uint256 taxAmount;
        bool isRegistered;
        bool isTaxPaid;
    }

    mapping(string => Vehicle) public vehicles;

    event VehicleRegistered(string licensePlate, uint256 entryTimestamp, uint256 taxAmount);
    event TaxPaid(string licensePlate, uint256 amount, address payer);

    function registerVehicle(string memory _licensePlate) public {
        require(!vehicles[_licensePlate].isRegistered, "Vehicle already registered");

        uint256 timestamp = block.timestamp;
        uint256 tax = calculateTax(timestamp);

        vehicles[_licensePlate] = Vehicle({
            licensePlate: _licensePlate,
            entryTimestamp: timestamp,
            taxAmount: tax,
            isRegistered: true,
            isTaxPaid: false
        });

        emit VehicleRegistered(_licensePlate, timestamp, tax);
    }

    function calculateTax(uint256 timestamp) internal pure returns (uint256) {
        uint256 hour = (timestamp / 60 / 60) % 24;

        if ((hour >= 7 && hour <= 10) || (hour >= 17 && hour <= 20)) {
            return 0.05 ether; // Higher congestion tax
        }
        return 0.02 ether; // Off-peak tax
    }

    function payTax(string memory _licensePlate) public payable {
        Vehicle storage vehicle = vehicles[_licensePlate];
        require(vehicle.isRegistered, "Vehicle not registered");
        require(!vehicle.isTaxPaid, "Tax already paid");
        require(msg.value >= vehicle.taxAmount, "Insufficient payment");

        vehicle.isTaxPaid = true;

        emit TaxPaid(_licensePlate, msg.value, msg.sender);
    }

    function getVehicle(string memory _licensePlate) public view returns (Vehicle memory) {
        require(vehicles[_licensePlate].isRegistered, "Vehicle not registered");
        return vehicles[_licensePlate];
    }

    // Owner can withdraw collected tax
    address public owner = msg.sender;

    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }
}