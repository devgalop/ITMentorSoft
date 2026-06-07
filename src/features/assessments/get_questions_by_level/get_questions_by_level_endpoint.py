from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_questions_by_level.get_questions_by_level_handler import (
    GetQuestionsByLevelHandler,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_request import (
    GetQuestionsByLevelRequest,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_response import (
    GetQuestionsByLevelResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_questions_by_level_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/questions/level/{difficulty}",
    status_code=200,
    summary="Get questions by difficulty level",
    description="Endpoint to retrieve all questions filtered by difficulty level.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Questions retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Questions retrieved successfully",
                        "questions": [
                            {
                                "question_id": "123e4567e89b12d3a456426614174000",
                                "text_to_evaluate": "Explain the difference between...",
                            }
                        ],
                    }
                }
            },
        },
        400: {
            "description": "Invalid request data.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Invalid request data."}
                }
            },
        },
        401: {
            "description": "Unauthorized.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Unauthorized."}
                }
            },
        },
        404: {
            "description": "Difficulty level not found.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Difficulty level not found.",
                    }
                }
            },
        },
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Internal server error.",
                    }
                }
            },
        },
    },
)
async def get_questions_by_level(
    difficulty: str,
    handler: Annotated[
        GetQuestionsByLevelHandler, Depends(get_get_questions_by_level_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "tutor"]))],
) -> GetQuestionsByLevelResponse:
    request = GetQuestionsByLevelRequest(difficulty=difficulty)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
