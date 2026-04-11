from unittest.mock import Mock, AsyncMock
import pytest

from src.features.user_management.login.login_handler import LoginHandler
from src.features.user_management.login.login_request import LoginRequest
from src.features.user_management.shared.token_generator import TokenResponse
from src.features.user_management.shared.user import User, UserRole, UserStatus

@pytest.mark.asyncio
async def test_when_credentials_are_valid_should_login_user():
    user_repository = AsyncMock()
    password_hasher = Mock()
    token_generator = Mock()
    
    user_repository.get_user_by_email = AsyncMock(return_value=User(
        username="testuser",
        email="test@example.com",
        password_hashed="hashed_password",
        status=UserStatus.ACTIVE,
        role = UserRole.STUDENT
    ))
    password_hasher.verify_password = Mock(return_value=True)
    token_generator.generate_token = Mock(return_value=TokenResponse(
        token="jwt_token",
        expiration_time=3600
    ))
    
    handler = LoginHandler(user_repository, password_hasher, token_generator)
    sample_pass = "Password123!"
    response = await handler.handle(LoginRequest(
        email="test@example.com",
        password=sample_pass
    ))
    assert response.is_successful == True
    assert response.token == "jwt_token"
    user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    password_hasher.verify_password.assert_called_once_with(sample_pass, "hashed_password")
    token_generator.generate_token.assert_called_once()