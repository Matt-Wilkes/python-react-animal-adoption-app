
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import jsonify, request, current_app
import time

from joserfc.jwk import RSAKey
from joserfc import jwt
from joserfc.jwt import JWTClaimsRegistry

load_dotenv()

secret = os.getenv('SECRET_KEY')
# current_app.config['SECRET_KEY']

access_claims_registry = JWTClaimsRegistry(
    iss={"essential": True, "value": "pawsforacause"},
    exp={"essential": True, "validate": True, "leeway": 60},
    token_type={"essential": True, "value": "access"}
)

refresh_claims_registry = JWTClaimsRegistry(
    iss={"essential": True, "value": "pawsforacause"},
    exp={"essential": True, "validate": True, "leeway": 60},
    token_type={"essential": True, "value": "refresh"}
)

# Encoding a JWT

def generate_token(user_id, additional_claims=None, token_type='access', expiry=3600):
    private_jwk = current_app.config['JWT_PRIVATE_KEY']
    current_time = int(time.time()) - 60
    
    header = {'alg': 'RS256'}
    
    claims = {
        "iss": "pawsforacause",
        "sub": str(user_id),
        "iat": current_time,
        "exp": current_time + expiry,
        "token_type": token_type
    }
    
    if additional_claims:
        claims.update(additional_claims)
    
    token = jwt.encode(header, claims, private_jwk)
    print(f'auth_routes time: {int(time.time())}')
    return token

def decode_token(token, token_type='access'):
    public_jwk = current_app.config['JWT_PUBLIC_KEY']
    
    try:
        token_obj = jwt.decode(token, public_jwk)
        claims = token_obj.claims

        if token_type == 'access':
            access_claims_registry.validate(claims)
        elif token_type == 'refresh':
            refresh_claims_registry.validate(claims)
        else:
            raise ValueError(f"Invalid token type: {token_type}")
        return token_obj  # This is a dictionary containing the token's data
    except Exception as e:
        # error_msg = str(e)
        # Handle errors such as invalid signature, expired token, etc.
        print(f"Token decoding failed: {e}")
        return None

def token_checker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"message": "Token is missing!"}), 401
        else:
            token = auth_header.split(" ")[1]
            
        if not token:
            return jsonify({"message": "Token is missing"}), 401
            
        try:
            valid_token = decode_token(token, token_type='access')
            
            if not valid_token:
                return jsonify({"message": "Invalid or expired token!"}), 401
            
            if valid_token.claims.get("token_type") != "access":
                return jsonify({"message": "Invalid token type!"}), 401
            
            user_id = valid_token.claims.get("id")
            
            if valid_token.claims.get("shelter_id"):
                request.shelter_id = valid_token.claims.get("shelter_id")
            
            if user_id is None:
                return jsonify({"message": "Token missing user_id"}), 401
            
            request.user_id = user_id
            
        except Exception as e:
            print(f"Error processing token claims: {str(e)}")
            return jsonify({"message": "Error processing authentication data"}), 401

        return f(*args, **kwargs)

    return decorated_function


# // Gather the values
# secret = readEnvironmentVariable("CSRF_SECRET") // HMAC secret key
# sessionID = session.sessionID // Current authenticated user session
# randomValue = cryptographic.randomValue() // Cryptographic random value

# // Create the CSRF Token
# message = sessionID.length + "!" + sessionID + "!" + randomValue.length + "!" + randomValue // HMAC message payload
# hmac = hmac("SHA256", secret, message) // Generate the HMAC hash
# csrfToken = hmac + "." + randomValue // Add the `randomValue` to the HMAC hash to create the final CSRF token. Avoid using the `message` because it contains the sessionID in plain text, which the server already stores separately.

# // Store the CSRF Token in a cookie
# response.setCookie("csrf_token=" + csrfToken + "; Secure") // Set Cookie without HttpOnly flag``

