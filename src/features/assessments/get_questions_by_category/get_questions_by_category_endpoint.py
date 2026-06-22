from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_questions_by_category.get_questions_by_category_handler import (
    GetQuestionsByCategoryHandler,
)
from src.features.assessments.get_questions_by_category.get_questions_by_category_request import (
    GetQuestionsByCategoryRequest,
)
from src.features.assessments.get_questions_by_category.get_questions_by_category_response import (
    GetQuestionsByCategoryResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_questions_by_category_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/questions/category/{category}",
    status_code=200,
    summary="Get questions by category",
    description="Endpoint to retrieve all questions filtered by content category.",
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
            "description": "Category not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Category not found."}
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
async def get_questions_by_category(
    category: str,
    handler: Annotated[
        GetQuestionsByCategoryHandler, Depends(get_get_questions_by_category_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetQuestionsByCategoryResponse:
    request = GetQuestionsByCategoryRequest(category=category)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
