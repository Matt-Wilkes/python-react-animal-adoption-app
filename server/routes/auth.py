from authlib.jose import jwt, JoseError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import jsonify, request

load_dotenv()

# Encoding a JWT

secret = os.getenv('SECRET_KEY')

def generate_token(user_id, additional_data=None):
    
    header = {'alg': 'HS256'}
    
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Token expiration time (timezone-aware)
        "iat": datetime.now(timezone.utc), 
    }
    
    if additional_data:
        payload.update(additional_data)
    
    token = jwt.encode(header, payload, secret)
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, secret)
        return payload  # This is a dictionary containing the token's data
    except JoseError as e:
        # Handle errors such as invalid signature, expired token, etc.
        print(f"Token decoding failed: {e}")
        return None

def token_checker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            payload = decode_token(token)
            print(payload)
            request.user_id = payload.get("user_id")
        except Exception as e:
            return jsonify({"message": "Invalid or expired token!"}), 401

        return f(*args, **kwargs)

    return decorated_function