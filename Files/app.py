from flask import Flask, jsonify, request
import json
import pymongo
from pymongo.errors import PyMongoError
from urllib.parse import quote_plus
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:5000", "http://127.0.0.1:5000"]}})

# MongoDB Atlas Configuration
username = quote_plus("rohitvpatil3") 
password = quote_plus("Rohitpatil@1") 
MONGO_URI = f"mongodb+srv://{username}:{password}@yd.nldhork.mongodb.net/?retryWrites=true&w=majority&appName=yd"
client = pymongo.MongoClient(MONGO_URI)
db = client['yd']
collection = db['submissions']

# Route to serve data from JSON file
@app.route('/api', methods=['GET'])
def get_data():
    try:
        with open('data.json') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid data"}), 400
    name = data['name']
    email = data['email']
    try:
        collection.insert_one({"name": name, "email": email})
        return jsonify({"message": "Data submitted successfully"}), 200
    except PyMongoError as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
