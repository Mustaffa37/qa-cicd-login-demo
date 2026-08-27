import requests

BASE_URL = "http://127.0.0.1:8000"

def test_api_valid_login():
    """TC_API_01: Valid credentials return 200 OK and authentication token"""
    payload = {
        "email": "admin@qa.com",
        "password": "Pass123!"
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
        "email": "admin@qa.com",
        "password": "WrongPassword!"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=payload)
    
    # Assertions
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid email or password"