import time
import uuid
from flask import Flask, jsonify
import pytest
from lib.database_connection import DatabaseConnection, db
from lib.models import Shelter, User, Animal
from lib.models.animal_repository import AnimalRepository


# https://docs.pytest.org/en/stable/how-to/fixtures.html
# This is a Pytest fixture.
# It creates an object that we can use in our tests.
# We will use it to create a database connection.


from app import create_app, bcrypt

@pytest.fixture
def app():
    # Create a new Flask app for testing
    app = create_app(test_config={'TESTING': True})
    return app
    
@pytest.fixture
def db_connection(app: Flask):
    # Create a new DatabaseConnection instance in test mode
    conn = DatabaseConnection(test_mode=True)
    conn.configure_app(app)
    
    with app.app_context():
        conn.reset_db()
    return conn
# use a pytest fixture to push a context for a specific test.
@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield

@pytest.fixture
def client(app):
    # app.config['TESTING'] = True 
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user(app_ctx):
    hashed_password = bcrypt.generate_password_hash('V@lidp4ss').decode('utf-8') 
    test_user = User(email = "Unique_test1@example.com",password = hashed_password,first_name = "Unique_test",last_name = "user",shelter = Shelter(name = "Example Shelter",location = "South London",email = "info@example.com",domain = "example.com", phone_number = "07123123123"))
    
    db.session.add(test_user)
    db.session.commit()
    
    yield test_user
    db.session.delete(test_user)
    db.session.commit()

@pytest.fixture
def auth_user(mocker):
    def _auth_user(user_id=1,shelter_id=1, **claims):
        iat = int(time.time()) - 100
        exp = int(time.time()) + 900
        mock_token = mocker.Mock()
        mock_token.claims = {
            "iss": "pawsforacause",
            "sub": user_id,
            "iat": iat,
            "exp": exp,
            "token_type": "access",
            "shelter_id": shelter_id
        }
        mocker.patch('routes.auth.decode_token', return_value=mock_token)
        mocker.patch('routes.auth.validate_token', return_value=None)
        return mock_token
    return _auth_user

@pytest.fixture  
def no_auth(mocker):
    """Mock failed authentication"""
    mocker.patch('routes.auth.decode_token', side_effect=Exception("Invalid token"))
    

@pytest.fixture
def animal_repository(app_ctx, db_connection):
    test_shelter = Shelter(
    name = "Example Shelter",
    location = "South London",
    email = "info@example.com",
    domain = "example.com",
    phone_number = "07123123123"
)
    test_shelter_2 = Shelter(
    name = "Example Shelter 2",
    location = "North London",
    email = "info@example2.com",
    domain = "example2.com",
    phone_number = "07321321321"
)
    test_animals = [
        Animal(
            id=uuid.UUID("fe96bf2a-7ef1-410a-887a-28a61f418304"),
            name="Test One",
            species="cat",
            age=1,
            breed="Maine Coon",
            location="London",
            male=True,
            bio="This is a test cat.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter
        ),
        Animal(
            id=uuid.UUID("bfd86d41-07df-4b0d-85e0-bec04f61094b"),
            name="Test Two",
            species="dog",
            age=2,
            breed="test breed",
            location="London",
            male=True,
            bio="This is a test dog.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter
        ),
        Animal(
            id=uuid.UUID("082ad5ad-ae09-4046-9b63-8d81b6fb6f0d"),
            name="Test Three",
            species="wolf",
            age=3,
            breed="werewolf",
            location="London",
            male=True,
            bio="This is a test werewolf.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=False,
            shelter=test_shelter
        ),
        Animal(
            id=uuid.UUID("04595568-1801-40d4-be13-bdbfe8ded0d8"),
            name="Test Four",
            species="Rabbit",
            age=3,
            breed="wereRabbit",
            location="London",
            male=True,
            bio="This is a test wereRabbit.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter_2
        ),
        Animal(
            id=uuid.UUID("f8f12b04-b612-48cc-b87d-058dee19b36e"),
            name="Test Five",
            species="Other",
            age=2,
            breed="Monkey",
            location="London",
            male=True,
            bio="This is a test Monkey.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter_2
        ),
    ]
    # with app.app_context():
    db_connection.seed_db(test_animals)
    
    repo = AnimalRepository(db)
    return repo, test_animals
