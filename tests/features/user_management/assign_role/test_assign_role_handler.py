from unittest.mock import AsyncMock
import pytest

from src.features.user_management.assign_role.assign_role_handler import (
    AssignRoleHandler,
)
from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)


@pytest.mark.asyncio
async def test_when_role_is_valid_then_should_assign_role_successfully():
    user_repository = AsyncMock()
    user_repository.get_available_roles = AsyncMock(
        return_value=["admin", "editor", "viewer"]
    )
    handler = AssignRoleHandler(user_repository)

    request = AssignRoleRequest(user_id="user123", role="editor")
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Role assigned successfully."
    user_repository.get_available_roles.assert_called_once()
    user_repository.assign_role_to_user.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_role_is_invalid_then_should_respond_with_error():
    user_repository = AsyncMock()
    user_repository.get_available_roles = AsyncMock(
        return_value=["admin", "editor", "viewer"]
    )
    handler = AssignRoleHandler(user_repository)

    request = AssignRoleRequest(user_id="user123", role="invalid_role")
    response = await handler.handle(request)

    assert not response.is_success
    assert response.message == "Invalid role specified."
    user_repository.get_available_roles.assert_called_once()
    user_repository.assign_role_to_user.assert_not_called()
