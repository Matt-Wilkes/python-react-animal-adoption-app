from flask_bcrypt import Bcrypt 
from flask import Blueprint, jsonify, request
from sqlalchemy import select

from lib.database_connection import db
from lib.models.user import User
from routes.auth import decode_token, generate_token
# from app import bcrypt



auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/token', methods=['POST'])
def login():
    from app import bcrypt
    data = request.get_json()
    req_email = data.get('email')
    req_password = data.get('password')
    user = db.session.scalar(select(User).filter_by(email=req_email))
    if not user:
        return jsonify({"error": "Email or password is incorrect"}), 401
    elif bcrypt.check_password_hash(user.password, req_password):
        token_data = {
        "id": user.id,
        "shelter_id": user.shelter_id
        }
        token = generate_token(req_email, token_data) #generate token here 
        data = decode_token(token) # decode token 
        return jsonify({"token": token.decode('utf-8'), "user_id": data.get('id'), "shelter_id": data.get('shelter_id')}), 200
    else:
        return jsonify({"error": "Email or password is incorrect"}), 401