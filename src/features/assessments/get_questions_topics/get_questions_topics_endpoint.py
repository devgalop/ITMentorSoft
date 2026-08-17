from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_questions_topics.get_questions_topics_handler import (
    GetQuestionsTopicsHandler,
)
from src.features.assessments.shared.dependencies import (
    get_get_questions_topics_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/topics",
    status_code=200,
    summary="Get all unique topics from the questions",
    description="Endpoint to retrieve all unique topics from the questions.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Topics retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Topics with status published retrieved successfully.",
                        "topics": ["Math", "Science", "History"],
                    }
                }
            },
        },
        400: {
            "description": "Invalid request data.",
        },
    },
)
async def get_questions_topics(
    handler: Annotated[
        GetQuestionsTopicsHandler, Depends(get_get_questions_topics_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher", "student"]))],
):
    response = await handler.handle()
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.message)
    return response
