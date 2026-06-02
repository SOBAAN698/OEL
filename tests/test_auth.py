import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService
from app.models.user_model import User

@patch("app.services.auth_service.get_connection")
def test_authenticate_success(mock_get_connection):
    # Set up mock database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configure mock to return a valid admin record
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "username": "admin",
        "password": "admin123"
    }
    
    # Run authentication
    user = AuthService.authenticate("admin", "admin123")
    
    # Assertions
    assert user is not None
    assert isinstance(user, User)
    assert user.username == "admin"
    assert user.password == "admin123"
    mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = %s", ("admin",))

@patch("app.services.auth_service.get_connection")
def test_authenticate_invalid_password(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "username": "admin",
        "password": "admin123"
    }
    
    # Attempt login with wrong password
    user = AuthService.authenticate("admin", "wrongpassword")
    
    assert user is None

@patch("app.services.auth_service.get_connection")
def test_authenticate_user_not_found(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None
    
    # Attempt login with non-existent user
    user = AuthService.authenticate("nonexistent", "password")
    
    assert user is None

def test_authenticate_empty_fields():
    with pytest.raises(ValueError, match="Username cannot be empty."):
        AuthService.authenticate("", "admin123")
        
    with pytest.raises(ValueError, match="Password cannot be empty."):
        AuthService.authenticate("admin", "")
        
    with pytest.raises(ValueError, match="Username cannot be empty."):
        AuthService.authenticate("   ", "admin123")
