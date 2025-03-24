
from pathlib import Path
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from lib.models.base import Base
import lib.models
from flask.cli import with_appcontext

import os
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent
load_dotenv(dotenv_path=env_path / '.env')

db = SQLAlchemy(model_class=Base)
class DatabaseConnection:
    
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        

    def _database_name(self):
        if self.test_mode:
            return os.getenv("TEST_DATABASE_NAME")
        else:
            return os.getenv("DEV_DATABASE_NAME")
    
    def _database_url(self):
        db_user = os.getenv("DATABASE_USER")
        db_password = os.getenv("DATABASE_PASSWORD")
        hostname = os.getenv("DATABASE_HOST")

        db_url = URL.create(
            drivername="postgresql",
            username=db_user,
            password=db_password,
            host=hostname,
            database=self._database_name()
        )
        return db_url
    
    def configure_app(self, app: Flask):
        """configure a flask app and set up a connection to the database"""
        # self.app = Flask(__name__) sits in app.py
        app.config['SQLALCHEMY_DATABASE_URI'] = self._database_url()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # app.config['SQLALCHEMY_ECHO'] = True
        
        # intialise SQLAlchemy with app
        db.init_app(app)
        
        # store ref to the app, lets DatabaseConnection keep track of which app is configured
        # allows other methods in the class to accept app instance if needed
        # enables use of self.app.app_context() 
        self.app = app 
        
        return app
    
    def check_connection(self):
        """Check a flask app has been configured"""
        if self.app is None:
            raise ValueError("No flask app has been configured")
        return self.app
    
    def reset_db(self):
        """Drop db tables and recreate"""
        with self.app.app_context():
            with db.session.begin():
                db.drop_all()
                db.create_all()
                print("Database has been reset")
    
    def seed_db(self, data):
        """Seed the database"""
        with self.app.app_context():
            with db.session.begin():
                db.session.add_all(data)
                print(f"Database has been seeded")
    
    