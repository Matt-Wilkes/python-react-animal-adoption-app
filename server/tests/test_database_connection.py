import pytest
from lib.database_connection import db
from sqlalchemy import select
from lib.models import User, Shelter



def test_database_connection_responds(app, db_connection):
    with app.app_context():
        db_connection.reset_db()
        with db.session.begin():
            test_user = User(email = "test@example.com",password = "password1",first_name = "test",last_name = "user",shelter = Shelter(
    name = "Example Shelter",
    location = "South London",
    email = "info@example.com",
    phone_number = "07123123123"
)
    )
            db.session.add(test_user)
            retrieved_user = db.session.execute(select(User).where(User.first_name == "test")).scalar_one()
            print(retrieved_user)
            print(retrieved_user)
            assert retrieved_user is not None