import pytest
import json

from sqlalchemy import select
from lib.models import User
from lib.database_connection import db

def test_valid_login_response( app_ctx,web_client, db_connection, test_user):
    """When a user logs in with valid credentials, 
    a 200 response should be returned"""
    response = web_client.post('/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 200
    
def test_incorrect_password_response( app_ctx,web_client, db_connection, test_user):
    """When a user logs in with an incorrect password, 
    a 401 response should be returned"""
    response = web_client.post('/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert response.status_code == 401
    
def test_incorrect_email_response( app_ctx,web_client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a 401 response should be returned"""
    response = web_client.post('/token', json={"email": "invalid_email@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 401
    
def test_incorrect_password_error_message( app_ctx,web_client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a generic error message should be returned 
    'Email or password is incorrect'
    """
    response = web_client.post('/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert response.json['error'] == 'Email or password is incorrect'
    
def test_incorrect_email_error_message( app_ctx,web_client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a generic error message should be returned 
    'Email or password is incorrect'
    """
    response = web_client.post('/token', json={"email": "invalid_email@example.com", "password": "V@lidp4ss"})
    assert response.json['error'] == 'Email or password is incorrect'
