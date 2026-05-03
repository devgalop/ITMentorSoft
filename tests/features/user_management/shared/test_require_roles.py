import pytest
from fastapi import HTTPException

from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData


def test_when_user_has_required_role_then_passes_and_returns_user():
    user = TokenData(user_name="alice", role="admin")
    checker = require_roles(["admin"])

    result = checker(user)

    assert result is user


def test_when_user_lacks_required_role_then_raises_http_403():
    user = TokenData(user_name="bob", role="student")
    checker = require_roles(["admin"])

    with pytest.raises(HTTPException) as exc_info:
        checker(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not enough permissions"


def test_when_multiple_roles_accepted_and_user_has_one_then_passes():
    user = TokenData(user_name="charlie", role="teacher")
    checker = require_roles(["admin", "teacher"])

    result = checker(user)

    assert result is user
