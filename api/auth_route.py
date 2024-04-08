from flask import Blueprint, request,jsonify
from pymongo import MongoClient
from bson import ObjectId
import re
import hashlib
import os
from dotenv import load_dotenv


db_host = os.getenv("DB_HOST")
# Connect to MongoDB
client = MongoClient(db_host)
db = client['flask_mongo_example']
users_collection = db['users']

auth_api = Blueprint('auth_api',__name__)

# Register user
# Register route
@auth_api.route('/register', methods=['POST'])
def register():
    try:
        # Extract data from request
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check if email already exists
        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already exists'}), 400

        # Hash password
        hashed_password = hash_password(password)

        # Insert user into database
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        result = users_collection.insert_one(user_data)

        # Return response
        user_id = str(result.inserted_id)
        return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Login route
@auth_api.route('/login', methods=['POST'])
def login():
    try:
        # Extract data from request
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Hash password
        hashed_password = hash_password(password)

        # Check if user exists
        user = users_collection.find_one({'email': email, 'password': hashed_password})
        if user:
            user_id = str(user['_id'])
            return jsonify({'message': 'Login successful', 'user_id': user_id}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def hash_password(password):
    # Choose a secure hashing algorithm (e.g., SHA-256)
    hash_algorithm = hashlib.sha256()
    # Encode the password string to bytes and hash it
    hash_algorithm.update(password.encode('utf-8'))
    # Return the hashed password as a hexadecimal string
    return hash_algorithm.hexdigest()
