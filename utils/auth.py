# utils/auth.py

from functools import wraps
import jwt
import datetime
from flask import request, jsonify, current_app

def generate_jwt(user_data):
    """Generates a JWT for the given user data."""
    payload = {
        'sub': user_data['username'],  # Subject: username
        'roles': user_data['roles'],  # User roles
        'iat': datetime.datetime.now(datetime.timezone.utc), # Issued At
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS']) # Expiration
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

def token_required(f):
    """Decorator to protect API routes, ensuring a valid JWT is present."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # Expects "Bearer <token>"
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.current_user = data['sub'] # Store username
            request.user_roles = data['roles'] # Store roles
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

def roles_required(roles):
    """Decorator to check if the authenticated user has any of the required roles."""
    def decorator(f):
        @wraps(f)
        @token_required # Ensure token is present before checking roles
        def decorated_function(*args, **kwargs):
            if not any(role in request.user_roles for role in roles):
                return jsonify({'message': 'Access denied: Insufficient permissions.'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator