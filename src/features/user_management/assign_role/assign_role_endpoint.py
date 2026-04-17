from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.user_management.shared.dependencies import get_assign_role_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
from src.features.user_management.assign_role.assign_role_response import (
    AssignRoleResponse,
)
from src.features.user_management.assign_role.assign_role_handler import (
    AssignRoleHandler,
)

router = APIRouter()


@router.put(
    "/assign-role",
    status_code=200,
    summary="Assign a role to a user",
    description="Assigns a specified role to a user based on the provided user ID and role information.",
    tags=["User Management"],
    responses={
        200: {
            "description": "Role assigned successfully. Returns a message indicating the successful role assignment.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Role assigned successfully.",
                    }
                }
            },
        },
        400: {
            "description": "Bad Request. Role assignment failed due to invalid user ID or role information.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "User not found or invalid role.",
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized. The request requires authentication.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
    },
)
async def assign_role(
    request: AssignRoleRequest,
    handler: Annotated[AssignRoleHandler, Depends(get_assign_role_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> AssignRoleResponse:
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
