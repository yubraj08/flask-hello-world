from flask import Blueprint, request,jsonify
import sqlite3
import re
import hashlib

auth_api = Blueprint('auth_api',__name__)

# Register user
@auth_api.route('/register', methods=['POST'])
def register():
    try:
        conn = sqlite3.connect('prediction.db')
        c = conn.cursor()
        username = request.json['username']
        email = request.json['email']
        password = hash_password(request.json['password'])

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if email already exists
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()
        if existing_user:
            conn.close()
            return jsonify({'error': 'Email already exists'}), 400
        
        # Check if username already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            conn.close()
            return jsonify({'error': 'Username already exists'}), 400
        
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Register user
@auth_api.route('/login', methods=['POST'])
def login():
    try:
        conn = sqlite3.connect('prediction.db')
        c = conn.cursor()
        username_or_email = request.json.get('username')
        password = hash_password(request.json['password'])

        # Check if username_or_email exists in either username or email column
        c.execute("SELECT * FROM users WHERE username=? OR email=?", (username_or_email, username_or_email))
        user = c.fetchone()
        
        if user:
            # Check if password matches
            if password == user[3]:  # Assuming password is stored at index 3 in the database
                conn.close()
                user_details = {'id': user[0], 'username': user[1], 'email': user[2]}
                return jsonify({'message': 'User created successfully', 'user': user_details}), 201
            else:
                conn.close()
                return jsonify({'error': 'Incorrect password'}), 401
        else:
            conn.close()
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def hash_password(password):
    # Choose a secure hashing algorithm (e.g., SHA-256)
    hash_algorithm = hashlib.sha256()
    # Encode the password string to bytes and hash it
    hash_algorithm.update(password.encode('utf-8'))
    # Return the hashed password as a hexadecimal string
    return hash_algorithm.hexdigest()
