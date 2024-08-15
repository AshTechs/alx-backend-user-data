#!/usr/bin/env python3

import requests

# Update these constants with appropriate values
EMAIL = "test@example.com"
PASSWORD = "securepassword"
NEW_PASSWORD = "newsecurepassword"
RESET_PASSWORD_EMAIL = "reset@example.com"

BASE_URL = "http://127.0.0.1:5000"

def register_user(email: str, password: str) -> None:
    """Register a user and check the response."""
    url = f"{BASE_URL}/users"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("User registered successfully.")

def log_in(email: str, password: str) -> str:
    """Log in with the user and return session ID."""
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Login successful.")
    return response.cookies.get("session_id")

def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with wrong password and check the response."""
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("Login attempt with wrong password.")

def access_profile(session_id: str) -> None:
    """Access user profile with a valid session ID."""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Accessed profile successfully.")
    print(response.json())

def reset_password(email: str) -> None:
    """Request a password reset token."""
    url = f"{BASE_URL}/reset_password"
    response = requests.post(url, data={"email": email})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    reset_token = response.json().get("reset_token")
    print("Password reset token received.")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using the reset token."""
    url = f"{BASE_URL}/reset_password"
    response = requests.put(url, data={"email": email, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Password updated successfully.")

if __name__ == "__main__":
    # Register a user
    register_user(EMAIL, PASSWORD)

    # Log in with correct credentials
    session_id = log_in(EMAIL, PASSWORD)

    # Log in with incorrect credentials
    log_in_wrong_password(EMAIL, "wrongpassword")

    # Access the profile of the logged-in user
    access_profile(session_id)

    # Reset the password
    reset_token = reset_password(RESET_PASSWORD_EMAIL)

    # Update the password
    update_password(RESET_PASSWORD_EMAIL, reset_token, NEW_PASSWORD)

    # Log in with the new password
    log_in(RESET_PASSWORD_EMAIL, NEW_PASSWORD)
