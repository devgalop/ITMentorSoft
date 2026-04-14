from src.features.user_management.recovery_password.recovery_password_request import RecoveryPasswordRequest
import pytest

def test_when_request_is_valid_then_exception_is_not_raised():
    request = RecoveryPasswordRequest(email="test@example.com")
    assert request.email == "test@example.com"
    
def test_when_email_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email is required"):
        RecoveryPasswordRequest(email="")

def test_when_email_is_invalid_then_exception_is_raised():
    with pytest.raises(ValueError, match="Invalid email format"):
        RecoveryPasswordRequest(email="invalid-email")
        
def test_when_email_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email must be no more than 255 characters long"):
        RecoveryPasswordRequest(email="a" * 256 + "@example.com")

def test_when_email_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email must be at least 5 characters long"):
        RecoveryPasswordRequest(email="a@b")