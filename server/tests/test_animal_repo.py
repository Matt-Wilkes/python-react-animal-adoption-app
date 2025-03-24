import pytest
from lib.database_connection import db
from sqlalchemy import select
from db.seed import test_animals
from lib.models import Animal, Shelter
from lib.models.animal_repository import AnimalRepository



def test_get_all_animals(app, animal_repository):
    """get_all should return all animals"""
    repo, test_animals = animal_repository
    
    with app.app_context():
        animals = repo.get_all()
        assert len(animals) == len(test_animals)
"""
get_all_active should return all animals where 'isActive' is True
"""
def test_get_all_active(app, animal_repository):
    repo, test_animals = animal_repository
    with app.app_context():
        active_animals = repo.get_all_active()
        assert len(active_animals) == 2
        
"""
get_by_id should return the animal with a matching id
"""
def test_get_by_id(app, animal_repository):
    repo, test_animals = animal_repository
    with app.app_context():
        animal = repo.get_by_id(3)
        assert animal.id == 3

"""
create_new_animal should create a new animal
"""
def test_create_new_animal(app, animal_repository):
    repo, test_animals = animal_repository

    animal_data = {
        'name':"new animal",
        "species" : "rabbit",
        "age" : 5,
        "breed" : "robot",
        "location" : "Cardiff",
        "male" : True,
        "bio" : "This is a lovely cyborg",
        "neutered" : True,
        "lives_with_children" : True,
        "image" : "",
        "isActive" : True,
        "shelter_id": 1
    }
    with app.app_context():
        repo.create_new_animal(animal_data)
        animal = db.session.scalar(select(Animal).filter_by(name="new animal"))
        animals = repo.get_all()

        assert animals[3].name == "new animal"
        assert animal.name == "new animal"
        assert len(animals) == len(test_animals)+1
