from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from src.features.user_management.shared.get_current_user import get_current_user
from src.features.user_management.shared.token_generator import (
    InvalidTokenError,
    TokenData,
)


def test_when_token_is_valid_then_returns_token_data():
    token_generator = MagicMock()
    token_generator.validate_token = MagicMock(
        return_value=TokenData(user_name="alice", role="admin")
    )

    result = get_current_user(token="valid-token", token_generator=token_generator)

    assert result.user_name == "alice"
    assert result.role == "admin"
    token_generator.validate_token.assert_called_once_with("valid-token")


def test_when_token_is_invalid_then_raises_http_401():
    token_generator = MagicMock()
    token_generator.validate_token = MagicMock(
        side_effect=InvalidTokenError("Bad token")
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalid-token", token_generator=token_generator)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid authentication credentials"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
