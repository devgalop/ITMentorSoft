from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_contents_by_category.get_contents_by_category_handler import (
    GetContentsByCategoryHandler,
)
from src.features.content_management.get_contents_by_category.get_contents_by_category_request import (
    GetContentsByCategoryPaginationRequest,
)
from src.features.content_management.get_contents_by_category.get_contents_by_category_response import (
    GetContentsByCategoryResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_contents_by_category_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/category/{criteria}",
    status_code=200,
    summary="Get contents by category",
    description="Endpoint to retrieve educational resource contents filtered by category with pagination support.",
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
            "description": "Not Found. No contents found for the given category.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No contents found for the given category",
                        "items": [],
                        "total": 0,
                    }
                }
            },
        },
    },
)
async def get_contents_by_category(
    criteria: str,
    handler: Annotated[
        GetContentsByCategoryHandler, Depends(get_get_contents_by_category_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "tutor", "student"]))],
    page: int = 0,
    page_size: int = 10,
) -> GetContentsByCategoryResponse:
    if not criteria:
        return GetContentsByCategoryResponse(
            is_success=False,
            message="Invalid category parameter. Category must be provided.",
            items=[],
            total=0,
        )
    request = GetContentsByCategoryPaginationRequest(
        category=criteria, page=page, page_size=page_size
    )
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
