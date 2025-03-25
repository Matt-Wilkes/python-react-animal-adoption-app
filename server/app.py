import click
from flask import Flask, request, render_template, redirect, jsonify, send_from_directory
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import select
# from lib.database_connection import db_session
from db.seed import Animal, Shelter, User, users, animals, shelters
from functools import wraps
from controllers.auth import generate_token, decode_token
from flask_bcrypt import Bcrypt 
from lib.database_connection import DatabaseConnection, db
from lib.models.animal_repository import AnimalRepository


# Photo upload
# from werkzeug.utils import secure_filename
# from flask import url_for
# from flask import send_from_directory
# from flask import abort
# import FileUploader
# End photo upload.

from dotenv import load_dotenv
import os

# Create a new Flask app
app = Flask(__name__)
conn = DatabaseConnection()
conn.configure_app(app)
# Encryption with Bcrypt
bcrypt = Bcrypt(app) 

CORS(app) 

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
# decorator function used for sake of DRY
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
            request.user_id = payload.get('user_id')
        except Exception as e:
            return jsonify({"message": "Invalid or expired token!"}), 401

        return f(*args, **kwargs)

    return decorated_function
# == Routes Here ==


# Listings route - return a list of all animals.
@app.route('/listings', methods=['GET'])
def display_animals():
    animals = AnimalRepository(db).get_all_active()
    return jsonify([animal.to_dict() for animal in animals]), 200



@app.route('/listings/<int:id>', methods= ['GET'])
def display_one_animal(id):
        animal = AnimalRepository(db).get_by_id(id)
        return jsonify(animal.to_dict()), 200


# THIS FUNCTION WILL POST A NEW ANIMAL TO THE DATABASE
# TODO : Will I need to change '/listings' to something else? 
@app.route('/listings', methods=['POST'])
@token_checker # Added this decorator to check for token. 
def create_new_animal():
    data = request.get_json()
    with app.app_context():
        animal = AnimalRepository(db).create_new_animal(data)
        return jsonify(animal.to_dict()), 201
   
        # below lines aren't needed until upload is implemented
        # retrieved_animal = db.session.get(Animal, animal.id)
        # retrieved_animal.image = f"unique_id_{retrieved_animal.id}"
        

        # Step b - Save the image into the static folder

        # uploader = FileUploader.FileUploader(
        #     upload_location=os.getenv("PHOTO_UPLOAD_LOCATION"),
        #     allowed_extensions=app.config['UPLOAD_EXTENSIONS']
        # )

        # uploaded_file = request.files['file']
        # success, message = uploader.validate_and_save(uploaded_file)

        # if not success:
        #     return message, 400
        # return jsonify(animal.as_dict()), 201

        

# This function allows a logged in user to edit information about a specific animal
@app.route('/listings/<int:id>', methods=['PUT'])
@token_checker  # Ensures that the user is authenticated
def update_animal(id):
    data = request.get_json()
    print('Received the data:', data)
    animal = AnimalRepository(db).update_animal(data)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404
    else:
        return jsonify(animal.to_dict()), 200



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
    with app.app_context():
        data = request.get_json()
        req_email = data.get('email')
        req_password = data.get('password')
        user = User.query.filter_by(email=req_email).first()
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