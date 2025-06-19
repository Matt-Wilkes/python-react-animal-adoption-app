import pytest
from lib.models.animal import Animal


"""
When there is a request GET /animals
It should return status code 200 OK
And the response should be a list of all ACTIVE animals
"""
def test_get_active_animals(app_ctx, db_connection, client, animal_repository):
    response = client.get('/animals')
    response_data = response.get_json()

    animal_names = [animal['name'] for animal in response_data]
    
    assert response.status_code == 200
    assert len(response_data) == 4
    assert "Test One" in animal_names
    assert "Test Two" in animal_names
    assert "Test Four" in animal_names
    assert "Test Five" in animal_names
    assert "Test Three" not in animal_names
    

# request GET /animals
# with path: 1
"""
When there is a request GET /animals/1
It should return status code 200 OK
And the response should be the animal with the id of 1
"""
def test_get_animals_with_id(app_ctx, db_connection, client, animal_repository):
    response = client.get('/animals/1')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '{"age":1,"bio":"This is a test cat.","breed":"Maine Coon","id":1,"images":1,"isActive":true,"lives_with_children":false,"location":"London","male":true,"name":"Test One","neutered":false,"profileImageId":null,"shelter_id":1,"species":"cat"}\n'
    

# request POST /animals
# with 
# expected response (201 OK)
"""
When there is a request POST /animals/
It should return status code 201 Created
And the response should be the new animal object
"""
def test_post_animal_route_logged_in(client, animal_repository, auth_user):
    auth_user()
    
    new_animal={
        "id": 4,
        "name":"Andie",
        "species":"cat",
        "age":8,
        "breed":"British Shorthair",
        "location":"Cardiff",
        "male":True,
        "bio":"This is a lovely cat and he needs a good home.",
        "neutered":True,
        "lives_with_children":True,
        "images":1,
        "profileImageId":"profile.png",
        "isActive":True,
        "shelter_id":1,
        }
    
    response = client.post('/animals', json=new_animal, headers={'Authorization': 'Bearer valid-token'})
    response_data = response.get_json()
    assert response.status_code == 201
    assert response_data['name'] == 'Andie'
    assert response_data['age'] == 8
    assert response_data['isActive'] == True
"""
When there is a request POST /animals/
It should return status code 201 Created
And the response should be the new animal object
"""

    
# request PUT /animals
# with path: 1
# expected response (200 OK)

"""
When there is a request PUT /animals/1
It should return status code 200 OK
And the response should be the updated animal id 1 object
"""

def test_update_animal_logged_in(client, animal_repository, auth_user):
    auth_user()
    animal_update={
        "id": 1,
        "name":"Andie 2.0",
        "species":"cat",
        "age":5,
        "breed":"British Shorthair",
        "location":"Cardiff",
        "male":True,
        "bio":"This is a lovely cat and he needs a good home.",
        "neutered":True,
        "lives_with_children":True,
        "images":1,
        "profileImageId":"profile.png",
        "isActive":True,
        "shelter_id":1,
        }
    
    response = client.put('/animals/1', json=animal_update, headers={'Authorization': 'Bearer valid-token'})
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['name'] == 'Andie 2.0'
    assert response_data['age'] == 5
    assert response_data['isActive'] == True
    
"""
When there is a request PUT /animals/5
WHERE the animal shelter_id does not match the user.shelter_id
It should return status code 403 Forbidden
And the response should be the updated animal id 1 object
"""

def test_cannot_update_animal_from_another_shelter(client, animal_repository, auth_user):
    auth_user()
    animal_update={
        "id": 5,
        "name":"Test Five",
        "species":"cat",
        "age":5,
        "breed":"British Shorthair",
        "location":"Cardiff",
        "male":True,
        "bio":"This is a lovely cat and he needs a good home.",
        "neutered":True,
        "lives_with_children":True,
        "images":1,
        "profileImageId":"profile.png",
        "isActive":True,
        "shelter_id":2,
        }
    
    response = client.put('/animals/5', json=animal_update, headers={'Authorization': 'Bearer valid-token'})
    response_data = response.get_json()
    assert response.status_code == 403
    assert response_data['error'] == "You do not have permission to update this animal"
    
"""
When there is a request PUT /animals/1
And the animal doesn't exist
It should return status code 404 NOT FOUND
"""
def test_update_none_existent_animal(client, animal_repository, auth_user):
    auth_user()
    
    animal_update={
        "id": 100,
        "name":"Andie 2.0",
        "species":"cat",
        "age":5,
        "breed":"British Shorthair",
        "location":"Cardiff",
        "male":True,
        "bio":"This is a lovely cat and he needs a good home.",
        "neutered":True,
        "lives_with_children":True,
        "images":1,
        "profileImageId":"profile.png",
        "isActive":True,
        "shelter_id":1,
        }
    
    response = client.put('/animals/100', json=animal_update, headers={'Authorization': 'Bearer valid-token'})
    
    assert response.status_code == 404
    assert response.json['error'] == 'Animal not found'