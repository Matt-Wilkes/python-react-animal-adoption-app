import pytest
from sqlalchemy import null


def test_create_public_user(user_repo):
    """
    create__user should create a user in the database
    and return the created user
    with a null shelter_id
    """
    repo = user_repo
    
    email = "test.user@example.com"
    hashed_password = "$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W"
    first_name="test"
    last_name="user"
    
    data = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "password": hashed_password,
  }
    
    result = repo.create_user(data)
    
    
    assert result.email == "test.user@example.com"
    assert result.first_name == "test"
    assert result.last_name == "user"
    assert result.shelter_id is None

def test_create_shelter_user(user_repo):
    """
    create_user should create a user in the database
    and return the created user
    with a valid shelter id
    """
    repo = user_repo
    
    email = "test.user@example.com"
    hashed_password = "$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W"
    first_name="test"
    last_name="user"
    
    data = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "password": hashed_password,
    "shelter_id": 1
  }
    
    result = repo.create_user(data)
    
    assert result.email == "test.user@example.com"
    assert result.first_name == "test"
    assert result.last_name == "user"
    assert result.shelter_id is 1

    
def test_update_user(user_repo):
    """
    update_user should update a user in the database
    and return the updated user
    """
    repo = user_repo
    
    updated_first_name = "Joe"
    updated_last_name = "Bloggs"
    user_id = 10
    data = {
        "first_name": updated_first_name,
        "last_name": updated_last_name
    }
    
    result = repo.update_user(user_id, data)
    assert result.first_name == "Joe"
    assert result.last_name == "Bloggs"
    assert result.email == "shelter_user@example.com"
    
def test_update_user_errors_if_missing_attr(user_repo):
    """
    update_user should update a user in the database
    and return the updated user
    """
    repo = user_repo
    
    updated_first_name = "Joe"
    updated_last_name = "Bloggs"
    user_id = 10
    data = {
        "first_name": updated_first_name,
        "surname": updated_last_name
    }
    
    with pytest.raises(AttributeError) as err:
        repo.update_user(user_id, data)
    error_message = str(err.value)
    print(error_message)
    
    assert error_message == "attribute surname doesn't exist"
