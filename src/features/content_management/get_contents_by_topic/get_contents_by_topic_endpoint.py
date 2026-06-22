from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_contents_by_topic.get_contents_by_topic_handler import (
    GetContentsByTopicHandler,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_request import (
    GetContentsByTopicPaginationRequest,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_response import (
    GetContentsByTopicResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_contents_by_topic_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/topic/{criteria}",
    status_code=200,
    summary="Get contents by topic",
    description="Endpoint to retrieve educational resource contents filtered by topic with pagination support.",
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
            "description": "Not Found. No contents found for the given topic.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No contents found for the given topic",
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
async def get_contents_by_topic(
    criteria: str,
    handler: Annotated[
        GetContentsByTopicHandler, Depends(get_get_contents_by_topic_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher", "student"]))],
    page: int = 0,
    page_size: int = 10,
) -> GetContentsByTopicResponse:
    if not criteria:
        return GetContentsByTopicResponse(
            is_success=False,
            message="Invalid topic parameter. Topic must be provided.",
            items=[],
            total=0,
        )
    request = GetContentsByTopicPaginationRequest(
        topic=criteria, page=page, page_size=page_size
    )
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
