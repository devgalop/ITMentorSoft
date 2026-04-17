from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.user_management.get_available_roles.get_available_roles_response import (
    GetAvailableRolesResponse,
)
from src.features.user_management.get_available_roles.get_available_roles_handler import (
    GetAvailableRolesHandler,
)
from src.features.user_management.shared.dependencies import (
    get_get_available_roles_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/available-roles",
    status_code=200,
    summary="Get Available Roles",
    description="Endpoint to retrieve the list of available roles in the system.",
    tags=["User Management"],
    responses={
        200: {
            "description": "A list of available roles.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "roles": ["admin", "user", "editor"],
                    }
                }
            },
        },
        400: {
            "description": "Failed to retrieve available roles.",
            "content": {
                "application/json": {"example": {"is_success": False, "roles": []}}
            },
        },
    },
)
async def get_available_roles(
    handler: Annotated[
        GetAvailableRolesHandler, Depends(get_get_available_roles_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> GetAvailableRolesResponse:
    response = await handler.handle()
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
