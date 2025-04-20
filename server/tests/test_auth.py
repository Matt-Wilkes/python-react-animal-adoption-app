import time
import pytest
import json

from sqlalchemy import select
from lib.models import User
from lib.database_connection import db

def test_valid_login_response( app_ctx,client, db_connection, test_user):
    """When a user logs in with valid credentials, 
    a 200 response should be returned"""
    response = client.post('api/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 200
    
def test_incorrect_password_response( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect password, 
    a 401 response should be returned"""
    response = client.post('api/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert response.status_code == 401
    
def test_incorrect_email_response( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a 401 response should be returned"""
    response = client.post('api/token', json={"email": "invalid_email@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 401
    
def test_incorrect_password_error_message( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a generic error message should be returned 
    'Email or password is incorrect'
    """
    response = client.post('api/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert response.json['error'] == 'Email or password is incorrect'
    
def test_incorrect_email_error_message( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a generic error message should be returned 
    'Email or password is incorrect'
    """
    response = client.post('api/token', json={"email": "invalid_email@example.com", "password": "V@lidp4ss"})
    assert response.json['error'] == 'Email or password is incorrect'
    
def test_valid_login_returns_token(app_ctx, client, db_connection, test_user):
    """When a user logs in with valid credentials, a token should be returned"""
    response = client.post('api/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert 'token' in response.json

def test_invalid_login_doesnt_return_token(app_ctx, client, db_connection, test_user):
    "when a user attempts login with invalid credentials, there shouldn't be a token in the response"
    response = client.post('api/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert 'token' not in response.json
    assert response.status_code == 401
    
def test_nonexistant_user_doesnt_return_token(app_ctx, client, db_connection, test_user):
    "when a non-existant user attempts login, there shouldn't be a token in the response"
    response = client.post('api/token', json={"email": "idontexist@example.com", "password": "inV@lidp4ss"})
    assert 'token' not in response.json
    assert response.status_code == 401
    
def test_valid_login_returns_token(app_ctx, client, db_connection, test_user):
    """When a user logs in with valid credentials, a token should be returned"""
    response = client.post('api/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert 'token' in response.json
    
def test_protected_route_with_valid_token(client, db_connection, test_user):
    """Test accessing a protected route with a valid token"""
    response = client.post('api/token', json={
        'email':test_user.email,
        'password':'V@lidp4ss'
    })
    
    token = response.json['token']

    response = client.get('api/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200

def test_protected_route_without_token(client, db_connection):
    """Test accessing a protected route without a token"""
    response = client.get('api/protected')
    assert response.status_code == 401
    assert response.json['message'] == 'Token is missing!'

def test_protected_route_with_invalid_token(client):
    invalid_token = 'ezJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwYXdzZm9yYWNhdXNlIiwic3ViIjoiVW5pcXVlX3Rlc3QxQGV4YW1wbGUuY29tIiwiaWF0IjoxNzQzNjAyMzA3LCJleHAiOjE3NDM2MDU5MDcsImlkIjoxLCJzaGVsdGVyX2lkIjoxfQ.Misuk7gFhRWIXIC7pZRfgm9oKczFXBO2kkkkkKeYZ1_OM8FylPFvVqMk1dou_Z6V_h7LsRtBnmscxMeStAVhBUqDfUQOJkDDmqTXODRGgm-Xc7NUQM4LLQ5QQJMKsMUVVvpxV6_XkjN5R6BzhKp3KGew9eK1tQAIwHP_09hRD9y6WEqer2R5VJtUpPb9wMY9WcHg30mWIOqbTXHhjsv-ay572-LRz2mHgmWC5EsrfpcaWxiJQmYpWYiQCTcKD0wuPvYh53f-JOY1fIoXkW7YCQ'
    """Test accessing a protected route with an invalid token"""
    response = client.get('api/protected', headers={
        'Authorization': f'Bearer {invalid_token}'
    })
    assert response.status_code == 401

def test_token_can_be_decoded_with_public_key(app_ctx, client, db_connection, test_user):
    """Test that a token can be decoded with the public key"""
    response = client.post('api/token', json={
        'email': test_user.email,
        'password':'V@lidp4ss'
    })
    token = response.json['token']
    
    from routes.auth import decode_token
    decoded = decode_token(token)
    
    # Assert the token was decoded successfully
    assert decoded is not None
    assert decoded.claims.get('sub') == test_user.email
    assert decoded.claims.get('id') == test_user.id
    

def test_expired_token_is_rejected(app_ctx, client, db_connection, test_user, mocker):  
    mocker.patch('routes.auth.time.time', return_value=1743521149)
    response = client.post('api/token', json={
        'email': test_user.email,
        'password': 'V@lidp4ss'
    })
    token = response.json['token']
    
    
    response = client.get('api/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid or expired token!'
    
def test_logout_removes_token(app_ctx, client, db_connection, test_user, mocker):  
    
    response = client.post('api/logout')
    
    cookie_header = response.headers.get('Set-Cookie')
    print(cookie_header)
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    assert 'refresh_token=' in cookie_header
    assert 'Max-Age=0' in cookie_header or 'Expires=' in cookie_header
    assert response.json['message'] == 'logged out successfully'