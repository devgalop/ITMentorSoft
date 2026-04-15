from src.features.user_management.get_user.get_user_request import GetUserRequest
import pytest

def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetUserRequest(user_id="test")
    assert request.user_id == "test"
    
def test_when_user_id_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Username is required"):
        GetUserRequest(user_id="")
        
def test_when_user_id_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Username must be at least 3 characters long"):
        GetUserRequest(user_id="ab")

def test_when_user_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Username must be no more than 20 characters long"):
        GetUserRequest(user_id="a" * 21)
        
def test_when_user_id_contains_invalid_characters_then_exception_is_raised():
    with pytest.raises(ValueError, match="Username must be alphanumeric and can include underscores"):
        GetUserRequest(user_id="invalid-username")