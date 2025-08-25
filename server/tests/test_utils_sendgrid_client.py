import os
import pytest
import requests
from utils.sendgrid_api_client import send_verification_email
from sendgrid.helpers.mail import SendGridException

    
def test_email_returns_202_response(app_ctx, mocker):
    """
    GIVEN a pin
    AND a token
    AND a recipient
    send_verification_email should return a 202 response
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='verification'
    )

    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]

    # Validate request_body contains the expected HTML
    assert "123456" in request_body["content"][0]["value"]
    assert "verify?token=jwt-token-here" in request_body["content"][0]["value"]
    assert request_body["personalizations"][0]["to"][0]["email"] == test_recipient
    assert request_body["from"]["email"] == "mattwilkesdev@gmail.com"
    
def test_verification_email_contains_verify_link(app_ctx, mocker):
    """
    GIVEN a type of 'verification'
    send_verification_email 
    should return a request body
    THAT contains verify in the body
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='verification'
    )
    
    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    
    assert "verify?token=jwt-token-here" in request_body["content"][0]["value"]
    
def test_verification_email_contains_verification_content(app_ctx, mocker):
    """
    GIVEN a type of 'verification'
    send_verification_email 
    should return a request body
    THAT contains correct verification content
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='verification'
    )
    
    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    
    assert "verify?token=jwt-token-here" in request_body["content"][0]["value"]
    assert "Your verification PIN is" in request_body["content"][0]["value"]
    assert "Please confirm your account" in request_body["content"][0]["value"]
    assert "Click here to verify" in request_body["content"][0]["value"]
    
def test_verification_email_contains_correct_subject(app_ctx, mocker):
    """
    GIVEN a type of 'verification'
    send_verification_email 
    should have a subject 'Your verification pin:'
    THAT contains correct verification content
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='verification'
    )
    
    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    print(request_body)
    
    assert "Your verification pin" in request_body["subject"]
def test_forgotten_password_email_contains_correct_subject(app_ctx, mocker):
    """
    GIVEN a type of 'forgotten-password'
    send_verification_email 
    should have a subject 'Reset your password:'
    THAT contains correct verification content
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='forgotten-password'
    )
    
    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    print(request_body)
    
    assert "Reset your password" in request_body["subject"]
  
    
def test_verification_email_contains_verification_content(app_ctx, mocker):
    """
    GIVEN a type of 'forgotten-password'
    send_verification_email 
    should return a request body
    THAT contains correct password reset content
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='forgotten-password'
    )
    
    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    
    assert "Your password reset PIN is" in request_body["content"][0]["value"]
    assert "Please follow the password reset link below" in request_body["content"][0]["value"]
    assert "Click here to reset your password" in request_body["content"][0]["value"]

    
def test_verification_email_contains_forgotten_password_link(app_ctx, mocker):
    """
    GIVEN a type of 'forgotten-password'
    send_verification_email 
    should return a request body
    THAT contains forgotten-password in the body
    """
    
    mock_response = mocker.Mock()
    mock_response.status_code = 202
    mock_response.body = "OK"
    mock_response.headers = {}
    
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    
    instance = mock_sg_client.return_value
    instance.client.mail.send.post.return_value = mock_response
    test_recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
    send_verification_email(
        recipient=test_recipient,
        pin="123456",
        token="jwt-token-here",
        type='forgotten-password'
    )

    assert instance.client.mail.send.post.call_count == 1

    request_body = instance.client.mail.send.post.call_args[1]["request_body"]

    # Validate request_body contains the expected HTML
    assert "password-reset?token=jwt-token-here" in request_body["content"][0]["value"]


def test_email_network_error(app_ctx, mocker):
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    instance = mock_sg_client.return_value
    
    instance.client.mail.send.post.side_effect = requests.exceptions.RequestException("Network error")
    
    with pytest.raises(requests.exceptions.RequestException) as err:
        send_verification_email(
            recipient="test@example.com",
            pin="123456",
            token="jwt-token-here",
            type='verification'
        )
    
    assert "Network error" in str(err.value)

def test_email_internal_server_error(app_ctx, mocker):
    mock_sg_client = mocker.patch("utils.sendgrid_api_client.sendgrid.SendGridAPIClient")
    instance = mock_sg_client.return_value
    
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.body = '{"error": "Internal server error"}'
    mock_response.headers = {"Content-Type": "application/json"}
    
    instance.client.mail.send.post.return_value = mock_response

    send_verification_email(
        recipient="test@example.com",
        pin="123456",
        token="jwt-token-here",
        type='verification'
    )

    assert instance.client.mail.send.post.call_count == 1
    request_body = instance.client.mail.send.post.call_args[1]["request_body"]
    assert "123456" in request_body["content"][0]["value"]

