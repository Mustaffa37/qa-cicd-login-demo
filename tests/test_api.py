import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USER_EMAIL = os.getenv("TEST_USER_EMAIL")
USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

def test_api_valid_login():
    """TC_API_01: Valid credentials return 200 OK and authentication token"""
    payload = {
        "email": USER_EMAIL,
        "password": USER_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/api/login", json=payload)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "token" in data

def test_api_invalid_password():
    """TC_API_02: Incorrect password returns 401 Unauthorized"""
    payload = {
        "email": USER_EMAIL,
        "password": "WrongPassword!"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=payload)
    
    # Assertions
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid email or password"