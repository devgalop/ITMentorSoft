from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.register_content.register_content_handler import (
    RegisterContentHandler,
)
from src.features.content_management.register_content.register_content_request import (
    RegisterContentRequest,
)
from src.features.content_management.register_content.register_content_response import (
    RegisterContentResponse,
)
from src.features.content_management.shared.dependencies import (
    get_register_content_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    summary="Register new content",
    description="Endpoint to register new content in the system.",
    tags=["Content Management"],
    responses={
        201: {
            "description": "Content registered successfully. Returns the ID of the newly registered content.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "content_id": "123e4567-e89b-12d3-a456-426614174000",
                        "message": "Content registered successfully.",
                    }
                }
            },
        },
        400: {
            "description": "Bad Request. Content registration failed due to invalid input data or content with the same title already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "content_id": None,
                        "message": "Content registration failed. Invalid input data or content with the same title already exists.",
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized. Content registration failed due to missing or invalid authentication.",
            "content": {"application/json": {"example": {"message": "Unauthorized."}}},
        },
    },
)
async def register_content(
    request: RegisterContentRequest,
    handler: Annotated[RegisterContentHandler, Depends(get_register_content_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin", "tutor"]))],
) -> RegisterContentResponse:

    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
