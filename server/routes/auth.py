
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

claims_requests = JWTClaimsRegistry(
    iss={"essential": True, "value": "pawsforacause"},
    exp={"essential": True, "validate": True}
)

# Encoding a JWT

def generate_token(user_id, additional_claims=None):
    private_jwk = current_app.config['JWT_PRIVATE_KEY']
    
    header = {'alg': 'RS256'}
    
    claims = {
        "iss": "pawsforacause",
        "sub": str(user_id),
        "iat": int(time.time()) -20,
        "exp": int(time.time()) + 3600,  
    }
    
    if additional_claims:
        claims.update(additional_claims)
    
    token = jwt.encode(header, claims, private_jwk)
    return token

def decode_token(token):
    public_jwk = current_app.config['JWT_PUBLIC_KEY']
    try:
        token_obj = jwt.decode(token, public_jwk)
        claims = token_obj.claims
        claims_requests.validate(claims)
        return token_obj  # This is a dictionary containing the token's data
    except Exception as e:
        # error_msg = str(e)
        # Handle errors such as invalid signature, expired token, etc.
        print(f"Token decoding failed in decode: {e}")
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
            
        try:
            valid_token = decode_token(token)
            if not valid_token:
                return jsonify({"message": "Invalid or expired token!"}), 401
            
            user_id = valid_token.claims.get("id")
            
            if valid_token.claims.get("shelter_id"):
                request.shelter_id = valid_token.claims.get("shelter_id")
            
            if user_id is None:
                return jsonify({"message": "Token missing user_id"}), 401
            
            request.user_id = valid_token.claims.get("id")
            
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

