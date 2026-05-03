from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_resource_content.get_resource_content_handler import (
    GetResourceContentHandler,
)
from src.features.content_management.get_resource_content.get_resource_content_request import (
    GetResourceRequest,
)
from src.features.content_management.get_resource_content.get_resource_content_response import (
    GetResourceContentResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_resource_content_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/{content_id}",
    status_code=200,
    summary="Get resource content by ID",
    description="Endpoint to retrieve a specific resource content by its content ID.",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Content retrieved successfully. Returns the requested content.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Content retrieved successfully",
                        "content": {
                            "content_id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Introduction to Python",
                            "summary": "A beginner-friendly guide to Python programming.",
                            "url": "https://example.com/python-intro",
                            "category": "novice",
                            "related_topics": ["Python", "Programming"],
                        },
                    }
                }
            },
        },
        404: {
            "description": "Not Found. The requested content does not exist.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Content not found",
                        "content": None,
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized. Missing or invalid authentication.",
            "content": {"application/json": {"example": {"message": "Unauthorized."}}},
        },
    },
)
async def get_resource_content(
    content_id: str,
    handler: Annotated[
        GetResourceContentHandler, Depends(get_get_resource_content_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "tutor", "student"]))],
) -> GetResourceContentResponse:

    request = GetResourceRequest(content_id=content_id)
    response = await handler.handle(request)

    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())

    return response
