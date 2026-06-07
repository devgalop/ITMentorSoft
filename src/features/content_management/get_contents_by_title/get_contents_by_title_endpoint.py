from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_contents_by_title.get_contents_by_title_handler import (
    GetContentsByTitleHandler,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_request import (
    GetContentsByTitlePaginationRequest,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_response import (
    GetContentsByTitleResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_contents_by_title_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/title/{criteria}",
    status_code=200,
    summary="Get contents by title",
    description="Endpoint to retrieve educational resource contents filtered by title substring with pagination support.",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Contents retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Contents retrieved successfully",
                        "items": [],
                        "total": 0,
                    }
                }
            },
        },
        400: {
            "description": "Invalid pagination parameters.",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid pagination parameters."}
                }
            },
        },
        401: {
            "description": "Unauthorized.",
            "content": {"application/json": {"example": {"message": "Unauthorized."}}},
        },
        404: {
            "description": "Not Found. No contents found matching the given title criteria.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No contents found matching the given title criteria",
                        "items": [],
                        "total": 0,
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "An error occurred while retrieving contents."
                    }
                }
            },
        },
    },
)
async def get_contents_by_title(
    criteria: str,
    handler: Annotated[
        GetContentsByTitleHandler, Depends(get_get_contents_by_title_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "tutor", "student"]))],
    page: int = 0,
    page_size: int = 10,
) -> GetContentsByTitleResponse:
    if not criteria:
        return GetContentsByTitleResponse(
            is_success=False,
            message="Invalid title parameter. Title must be provided.",
            items=[],
            total=0,
        )
    request = GetContentsByTitlePaginationRequest(
        title=criteria, page=page, page_size=page_size
    )
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
