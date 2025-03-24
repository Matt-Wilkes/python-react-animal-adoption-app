from sqlalchemy import select
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