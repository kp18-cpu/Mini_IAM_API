# app.py

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime, timezone

from config import USERS_DB, SECRET_KEY
from utils.auth import generate_jwt, token_required, roles_required

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY # Load from config
app.config['USERS_DB'] = USERS_DB # Load from config
app.config['JWT_EXPIRATION_HOURS'] = 1 # Directly set or load from config.py

# --- Helper functions for our simple JSON 'database' ---
def load_users():
    if not os.path.exists(app.config['USERS_DB']) or os.stat(app.config['USERS_DB']).st_size == 0:
        return []
    with open(app.config['USERS_DB'], 'r') as f:
        return json.load(f)

def save_users(users):
    with open(app.config['USERS_DB'], 'w') as f:
        json.dump(users, f, indent=4)

# --- API Routes ---
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Mini IAM API!"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    users = load_users()
    if any(u['username'] == username for u in users):
        return jsonify({'message': 'User already exists'}), 409

    # Hash the password for security
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    new_user = {
        'username': username,
        'password_hash': hashed_password,
        'roles': ['user'] # Default role for new users
    }
    users.append(new_user)
    save_users(users)

    return jsonify({'message': 'User registered successfully', 'username': username}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    users = load_users()
    user = next((u for u in users if u['username'] == username), None)

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate JWT upon successful login
    token = generate_jwt(user)
    return jsonify({'message': 'Login successful', 'token': token}), 200

@app.route('/api/user_data', methods=['GET'])
@token_required
def get_user_data():
    """Accessible by any authenticated user."""
    return jsonify({
        'message': f'Welcome, {request.current_user}! This is your personal data.',
        'your_roles': request.user_roles,
        'data': {'item1': 'value1', 'item2': 'value2'}
    }), 200

@app.route('/api/admin_panel', methods=['GET'])
@roles_required(['admin'])
def get_admin_panel():
    """Accessible only by users with the 'admin' role."""
    return jsonify({
        'message': f'Hello, Admin {request.current_user}! This is the admin panel.',
        'your_roles': request.user_roles,
        'admin_secrets': ['secret_key_1', 'secret_key_2']
    }), 200

@app.route('/api/all_users', methods=['GET'])
@roles_required(['admin']) # Also requires admin role
def get_all_users():
    """Accessible only by users with the 'admin' role, lists all users."""
    users = load_users()
    # Return user details, but exclude password hashes for security
    user_list = [{"username": u["username"], "roles": u["roles"]} for u in users]
    return jsonify({"users": user_list}), 200


if __name__ == '__main__':
    # Ensure users.json exists, if not, create it
    if not os.path.exists(USERS_DB):
        with open(USERS_DB, 'w') as f:
            json.dump([], f)
    
    # Optionally, create a default admin user if the file is empty
    users_data = load_users()
    if not users_data:
        print("No users found. Creating default 'admin' user...")
        admin_password = "adminpassword" # Just default one, change it accordingly
        # Hash the password for security
        admin_hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
        default_admin = {
            "username": "admin",
            "password_hash": admin_hashed_password,
            "roles": ["user", "admin"]
        }
        users_data.append(default_admin)
        save_users(users_data)
        print(f"Default admin user 'admin' created with password '{admin_password}'. PLEASE CHANGE IT!")

    app.run(debug=True, port=5000)