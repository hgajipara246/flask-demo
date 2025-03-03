from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS

# MongoDB Configuration
MONGO_URI = "mongodb://harshilgajipara5:oIJmvmuEt0KJQIiV@localhost:27017/?authSource=admin"
client = MongoClient(MONGO_URI)
db = client['mydatabase']  # Database name
users_collection = db['users']  # Collection name

# Convert MongoDB ObjectId to string
def to_json(user):
    user["_id"] = str(user["_id"])
    return user

# Create User (POST)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("age"):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = {
        "name": data["name"],
        "email": data["email"],
        "age": data["age"]
    }
    result = users_collection.insert_one(new_user)
    return jsonify({"message": "User created", "id": str(result.inserted_id)}), 201

# Read All Users (GET)
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    return jsonify([to_json(user) for user in users])

# Read Single User (GET)
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = users_collection.find_one({"_id": ObjectId(id)})
        return jsonify(to_json(user)) if user else jsonify({"error": "User not found"}), 404
    except:
        return jsonify({"error": "Invalid user ID"}), 400

# Update User (PUT)
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID"}), 400

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        updated_user = {
            "name": data["name"],
            "email": data["email"],
            "age": data["age"],
        }
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
        return jsonify({"message": "User updated successfully"})
    except:
        return jsonify({"error": "Invalid request"}), 400

# Delete User (DELETE)
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        result = users_collection.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "User deleted"}) if result.deleted_count else jsonify({"error": "User not found"}), 404
    except:
        return jsonify({"error": "Invalid user ID"}), 400

if __name__ == '__main__':
    app.run(debug=True)
