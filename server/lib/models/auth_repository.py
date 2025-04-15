from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from lib.models.user import User
from routes.auth import decode_token, generate_token


class AuthRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
        
    def get_token(self, data):
        from app import bcrypt
        req_email = data.get('email')
        req_password = data.get('password')
        user = self.db.session.scalar(select(User).filter_by(email=req_email))
        if not user:
            return jsonify({"error": "Email or password is incorrect"}), 401
        elif bcrypt.check_password_hash(user.password, req_password):
            token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
            access_token = generate_token(req_email, token_data, token_type='access', expiry=900) 
            refresh_token = generate_token(req_email, {"token_type": "refresh"}, token_type='refresh', expiry=604800) 
            response = jsonify({"token": access_token,
                            "user": {
                                "id": user.id,
                                "shelter_id": user.shelter_id
                                },
                            })
            response.set_cookie('refresh_token',
                                refresh_token,
                                httponly=True,
                                secure=False, # set to True in Prod
                                samesite='Lax',
                                max_age=604800,
                                path='/'
                                )
            return response, 200
        else:
            return jsonify({"error": "Email or password is incorrect"}), 401
    
    def get_access_token(self, refresh_token):
        if not refresh_token:
            print("No refresh token provided in request")
            return jsonify({"error": "No refresh_token provided"}), 401
        try:
            decoded = decode_token(refresh_token)
            
            print(f"Decoded refresh token: {decoded}")
            
            if decoded.get('token_type') != 'refresh':
                print(f"Invalid token type: {decoded.get('token_type')}")
                return jsonify({"error":"Invalid token type"}), 401
            user_email = decoded.get('sub')
            
            user = self.db.session.scalar(select(User).filter_by(email=user_email))
            
            if not user:
                return jsonify({"error": "User not found"}), 401
            
            token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
            
            new_access_token = generate_token(user_email, token_data, token_type='access', expiry=900) 
            
            return jsonify({"token": new_access_token}), 200
        
        except Exception as e:
            print(f"Refresh token error: {e}")
            return jsonify({"error": "Invalid or expired refresh token"}), 401
        