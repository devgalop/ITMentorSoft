from fastapi import APIRouter, Depends
from typing import Annotated

from src.features.content_management.get_all_contents.get_all_contents_handler import (
    GetAllContentsHandler,
)
from src.features.content_management.get_all_contents.get_all_contents_request import (
    GetAllContentsRequest,
)
from src.features.content_management.get_all_contents.get_all_contents_response import (
    GetAllContentsResponse,
)
from src.features.content_management.shared.dependencies import (
    get_all_contents_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/",
    status_code=200,
    summary="Get all contents",
    description="Endpoint to retrieve all educational resource contents with pagination support.",
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
        401: {
            "description": "Unauthorized.",
            "content": {"application/json": {"example": {"message": "Unauthorized."}}},
        },
    },
)
async def get_all_contents(
    page: int,
    page_size: int,
    handler: Annotated[GetAllContentsHandler, Depends(get_all_contents_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher", "student"]))],
) -> GetAllContentsResponse:
    if page < 0 or page_size <= 0:
        return GetAllContentsResponse(
            is_success=False,
            message="Invalid pagination parameters. Page must be >= 0 and page_size must be > 0.",
            items=[],
            total=0,
        )
    request = GetAllContentsRequest(page=page, page_size=page_size)
    return await handler.handle(request)
