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

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Dictionary to store location data
location_data = {
    "latitude": None,
    "longitude": None,
    "timestamp": None
}

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    location_data['latitude'] = data.get('latitude')
    location_data['longitude'] = data.get('longitude')
    location_data['timestamp'] = time.time()
    print("Received location:", location_data)
    return jsonify({"status": "Location updated"}), 200

@app.route('/get_location', methods=['GET'])
def get_location():
    return jsonify(location_data), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable if available
    app.run(host='0.0.0.0', port=port)
