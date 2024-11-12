# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import time

# app = Flask(__name__)
# CORS(app)  # Allow cross-origin requests

# # Dictionary to store location data
# location_data = {
#     "latitude": None,
#     "longitude": None,
#     "timestamp": None
# }

# @app.route('/update_location', methods=['POST'])
# def update_location():
#     data = request.json
#     location_data['latitude'] = data.get('latitude')
#     location_data['longitude'] = data.get('longitude')
#     location_data['timestamp'] = time.time()
#     print("Received location:", location_data)
#     return jsonify({"status": "Location updated"}), 200

# @app.route('/get_location', methods=['GET'])
# def get_location():
#     return jsonify(location_data), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# import os
# import time
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient

# app = Flask(__name__)
# CORS(app)  # Allow cross-origin requests

# # Connect to MongoDB (replace with your MongoDB connection string)
# client = MongoClient("mongodb+srv://naved:12345@cluster0.gevcl.mongodb.net/")
# db = client["mydatabase"]
# collection = db["locations"]

# @app.route('/update_location', methods=['POST'])
# def update_location():
#     data = request.json
#     name = data.get('name')
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
#     timestamp = time.time()

#     # Insert data into MongoDB
#     if name and latitude is not None and longitude is not None:
#         location_entry = {
#             "name": name,
#             "latitude": latitude,
#             "longitude": longitude,
#             "timestamp": timestamp
#         }
#         collection.insert_one(location_entry)
#         print("Received and stored location:", location_entry)
#         return jsonify({"status": "Location updated"}), 200
#     else:
#         return jsonify({"error": "Invalid data"}), 400

# @app.route('/get_location', methods=['GET'])
# def get_location():
#     # Retrieve the latest location entry
#     location_entry = collection.find_one(sort=[("timestamp", -1)])
#     if location_entry:
#         location_entry["_id"] = str(location_entry["_id"])  # Convert ObjectId to string for JSON serialization
#         return jsonify(location_entry), 200
#     else:
#         return jsonify({"error": "No location data found"}), 404

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable if available
#     app.run(host='0.0.0.0', port=port)


import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Connect to MongoDB
client = MongoClient("mongodb+srv://naved:12345@cluster0.gevcl.mongodb.net/")
db = client["mydatabase"]
collection = db["locations"]

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = time.time()

    if name and latitude is not None and longitude is not None:
        # Use `name` as the unique identifier and upsert the document
        location_entry = {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp
        }
        # Update if `name` exists, insert if it doesn't
        result = collection.update_one(
            {"name": name},  # Query to match an existing document by name
            {"$set": location_entry, "$setOnInsert": {"name": name}},  # Update latitude, longitude, timestamp
            upsert=True  # Insert a new document if `name` does not exist
        )
        if result.matched_count > 0:
            print(f"Updated location for '{name}':", location_entry)
        else:
            print(f"Inserted new location for '{name}':", location_entry)
        
        return jsonify({"status": "Location updated"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/get_location', methods=['GET'])
def get_location():
    # Retrieve the latest location entry
    location_entry = collection.find_one(sort=[("timestamp", -1)])
    if location_entry:
        location_entry["_id"] = str(location_entry["_id"])  # Convert ObjectId to string for JSON serialization
        return jsonify(location_entry), 200
    else:
        return jsonify({"error": "No location data found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable if available
    app.run(host='0.0.0.0', port=port)

