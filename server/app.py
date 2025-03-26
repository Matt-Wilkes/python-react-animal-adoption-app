import click
from flask import Flask, request, jsonify, send_from_directory
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import select
from db.seed import Animal, User, users, animals, shelters
from routes.auth import generate_token, decode_token, token_checker
from flask_bcrypt import Bcrypt 
from lib.database_connection import DatabaseConnection, db
from routes.animal_routes import animal_bp


# Photo upload
# from werkzeug.utils import secure_filename
# import FileUploader
# End photo upload.

from dotenv import load_dotenv
import os

# Create a new Flask app
app = Flask(__name__)
conn = DatabaseConnection()
conn.configure_app(app)


CORS(app)

app.register_blueprint(animal_bp, url_prefix='/listings')


# Encryption with Bcrypt
bcrypt = Bcrypt(app) 

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Drop db tables and recreate"""
    with db.session.begin():
        db.drop_all()
        db.create_all()
        click.echo("Database has been created")
        
@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Drop db tables and recreate"""
    with db.session.begin():
        db.session.add_all(animals)
        db.session.add_all(users)
        click.echo("Database has been seeded")

app.cli.add_command(init_db_command)
app.cli.add_command(seed_db_command)

# ------------------------------------

# == Routes Here ==
# This backend function allows a user to update the isActive field in the database 
# This is mainly used when the user wants to 'hide' an animal profile by setting isActive to false

@app.route('/listings/<int:id>/change_isactive', methods=['PUT'])
@token_checker 
def update_is_active(id):
    with app.app_context():
        animal = Animal.query.get(id)
        if not animal:
            return jsonify({"message": "Animal not found"}), 404
        
        data = request.get_json()
        animal.isActive = data.get('isActive', animal.isActive)
        
        db.session.commit()
        return jsonify(animal.as_dict()), 200
    
@app.route('/token', methods=['POST'])
def login():
    data = request.get_json()
    req_email = data.get('email')
    req_password = data.get('password')
    user = db.session.scalar(select(User).filter_by(email=req_email))
    if not user:
        return jsonify({"error": "User not found"}), 401
    elif bcrypt.check_password_hash(user.password, req_password):
        token_data = {
        "id": user.id,
        "shelter_id": user.shelter_id
        }
        token = generate_token(req_email, token_data) #generate token here 
        data = decode_token(token) # decode token 
        return jsonify({"token": token.decode('utf-8'), "user_id": data.get('id'), "shelter_id": data.get('shelter_id')}), 200
    else:
        return jsonify({"error": "Password is incorrect"}), 401

# This function adds a new user to the database
@app.route('/sign-up', methods=['POST'])
def signup():
    with app.app_context():
        data = request.get_json()
        print('Received the data:', data)
        req_email = data.get('email')
        # Password hashing happens here
        plaintext_password = data['password']
        hashed_password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8') 

        # Shelter_id assignment via email domain name happens here
        # shelter_id = None
        # for domain, id in email_to_shelter_mapping.items():
        #     if domain in req_email:
        #         shelter_id = id
        #         break

        #     if shelter_id is None:
        #         return jsonify({'error': 'You do not have a registered animal shelter email'}), 400

        user = User(
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            # shelter_id=shelter_id
            shelter_id = data['shelter_id']
        )
        db.session.add(user)
        db.session.commit()
        token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
        token = generate_token(req_email, token_data)
        data = decode_token(token)
        return jsonify({"token": token.decode('utf-8'), "user_id": data.get('id'), "shelter_id": data.get('shelter_id')}), 201
        # return jsonify(user.as_dict()), 201

# test protected route
@app.route('/protected', methods=['GET'])
@token_checker
def protected_route():
    return jsonify({"message": f"Access granted, user_id: {request.user_id}"}), 200

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True)
    

        

############ Photo Upload.

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

# # Test to allow system admin to view files.
# @app.route('/upload', methods=['GET'])
# def upload_form():
#     file_listing = os.listdir(os.getenv("PHOTO_UPLOAD_LOCATION"))
#     return render_template('upload.html', file_listing = file_listing)

# @app.route('/upload', methods=['POST'])
# def upload_files():
#     uploader = FileUploader.FileUploader(
#         upload_location=os.getenv("PHOTO_UPLOAD_LOCATION"),
#         allowed_extensions=app.config['UPLOAD_EXTENSIONS']
#     )

#     uploaded_file = request.files['file']
#     success, message = uploader.validate_and_save(uploaded_file)

#     if not success:
#         return message, 400
#     return '', 204

# 
@app.route('/upload/<filename>')
def upload(filename):
    return send_from_directory(os.getenv("PHOTO_UPLOAD_LOCATION"), filename)

# # Validator for Dropzone js component.
# @app.errorhandler(413)
# def too_large(e):
#     return "File is too large", 413

############ End Photo Upload