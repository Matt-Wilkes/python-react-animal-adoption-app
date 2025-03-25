from sqlalchemy import select, update
from lib.models.animal import Animal
from flask_sqlalchemy import SQLAlchemy

class AnimalRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
    
    def get_all(self):
        return self.db.session.scalars(select(Animal)).all()
    
    def get_all_active(self):
        with self.db.session.begin():
            return self.db.session.scalars(select(Animal).where(Animal.isActive == True)).all()
        
    def get_by_id(self, animal_id):
        with self.db.session.begin():
            return self.db.session.scalar(select(Animal).filter_by(id=animal_id))
    
    def create_new_animal(self, data):
        with self.db.session.begin():
            # data = request.get_json()
            print('Received the data:', data)

            animal = Animal(
                name=data['name'],
                species=data['species'],
                age=data['age'],
                breed=data['breed'],
                location=data['location'],
                male=data['male'],
                bio=data['bio'],
                neutered=data['neutered'],
                lives_with_children=data['lives_with_children'],
                image = data['image'],
                shelter_id=data['shelter_id'],
            )

            self.db.session.add(animal)
            return animal
        
    def update_animal(self, data):
        with self.db.session.begin():
            # values = str(data)
            stmt = (update(Animal).where(Animal.id == data["id"]).values(data).returning(Animal))
            updated_animal = self.db.session.scalar(stmt)
            print(updated_animal)
            return updated_animal
            