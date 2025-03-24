from flask import Flask
import pytest
from lib.database_connection import DatabaseConnection, db
from db.seed import test_animals
from lib.models import Shelter, User, Animal
from lib.models.animal_repository import AnimalRepository


# This is a Pytest fixture.
# It creates an object that we can use in our tests.
# We will use it to create a database connection.
@pytest.fixture
def app():
    app = Flask(__name__)
    return app
    
@pytest.fixture
def db_connection(app: Flask):
    # Create a new DatabaseConnection instance in test mode
    conn = DatabaseConnection(test_mode=True)
    conn.configure_app(app)
    
    with app.app_context():
        conn.reset_db()
    return conn

@pytest.fixture
def animal_repository(app, db_connection):
    test_shelter = Shelter(
    name = "Example Shelter",
    location = "South London",
    email = "info@example.com",
    phone_number = "07123123123"
)
    test_animals = [
        Animal(
            name="Test One",
            species="cat",
            age=1,
            breed="Maine Coon",
            location="London",
            male=True,
            bio="This is a test cat.",
            neutered=False,
            lives_with_children=False,
            image="seed_cinnamon.png",
            isActive=True,
            shelter=test_shelter
        ),
        Animal(
            name="Test Two",
            species="dog",
            age=2,
            breed="test breed",
            location="London",
            male=True,
            bio="This is a test dog.",
            neutered=False,
            lives_with_children=False,
            image="seed_cinnamon.png",
            isActive=True,
            shelter=test_shelter
        ),
        Animal(
            name="Test Three",
            species="wolf",
            age=3,
            breed="werewolf",
            location="London",
            male=True,
            bio="This is a test werewolf.",
            neutered=False,
            lives_with_children=False,
            image="seed_cinnamon.png",
            isActive=False,
            shelter=test_shelter
        )
    ]
    with app.app_context():
        db_connection.seed_db(test_animals)
    
    repo = AnimalRepository(db)
    return repo, test_animals

# @pytest.fixture
# def db_session(app: Flask, db_connection):
#     """Provides a transaction-managed SQLAlchemy session,
#     therefore it isn't necessary to call session.begin() within tests
#     """
#     with app.app_context():
#         db.session.begin_nested()
#         yield db.session
        
#         db.session.rollback()
#         db.session.close()

# @pytest.fixture # This is a factory fixture
# def seeded_db(app: Flask, db_connection):
#     """This is a factory fixture to reset and seed the database. A list of test data should be passed in as an argument. When called it will create and return the inner function _seed_with"""
#     def _seed_with(test_data): # This ahs access to the app and db_connection through closure
#         with app.app_context():
#             db_connection.reset_db()  # Ensure clean state
#             db_connection.seed_db(test_data)
#         return db_connection
    
#     return _seed_with

# fixture to use Flask app context
# @pytest.fixture
# def app_context(app):
#     with app.app_context() as context:
#         # yield passes control and context to test function
#         # cleans up after execution
#         yield context

# @pytest.fixture
# def created_animals_repo(app, db_connection):
#     from lib.database_connection import db
#     db_connection.reset_db()
#     db_connection.seed_db(test_animals)
#     animals_repo = AnimalRepository(db)
#     return animals_repo, app