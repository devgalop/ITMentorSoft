from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_question_by_id.get_question_by_id_handler import (
    GetQuestionByIdHandler,
)
from src.features.assessments.get_question_by_id.get_question_by_id_request import (
    GetQuestionByIdRequest,
)
from src.features.assessments.get_question_by_id.get_question_by_id_response import (
    GetQuestionByIdResponse,
)
from src.features.assessments.shared.dependencies import get_get_question_by_id_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/questions/{question_id}",
    status_code=200,
    summary="Get a question by ID",
    description="Endpoint to retrieve a full question with its rubric by its ID.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Question retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Question retrieved successfully",
                        "question": {
                            "question_id": "123e4567e89b12d3a456426614174000",
                            "text": "Explain the difference between...",
                            "concept": "Concept name",
                            "definition": "Definition text",
                            "simple_explanation": "Simple explanation",
                            "correct_sample": "Correct sample text",
                            "wrong_sample": "Wrong sample text",
                            "common_misconception": [
                                "Misconception 1",
                                "Misconception 2",
                            ],
                            "rubric": [{"score": 3, "explanation": "Excellent answer"}],
                            "semantic_keywords": ["keyword1", "keyword2"],
                            "status": "draft",
                        },
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
            "description": "Question not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Question not found"}
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
async def get_question_by_id(
    question_id: str,
    handler: Annotated[GetQuestionByIdHandler, Depends(get_get_question_by_id_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetQuestionByIdResponse:
    request = GetQuestionByIdRequest(question_id=question_id)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
