from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import pymongo
from pymongo.errors import PyMongoError
from urllib.parse import quote_plus

app = Flask(__name__)

# MongoDB Atlas Configuration
username = quote_plus("rohitvpatil3")  # Replace with your actual username
password = quote_plus("Rohitpatil@1")   # Replace with your actual password
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

# Route to render form
@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        try:
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for('success'))
        except PyMongoError as e:
            error = f"An error occurred: {str(e)}"
    return render_template('form.html', error=error)

# Success Page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
