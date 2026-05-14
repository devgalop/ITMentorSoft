from typing import Annotated

from fastapi import APIRouter, Depends

from src.features.assessments.register_question.register_question_handler import (
    RegisterQuestionHandler,
)
from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from src.features.assessments.register_question.register_question_response import (
    RegisterQuestionResponse,
)
from src.features.assessments.shared.dependencies import get_register_question_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.post(
    "/register",
    status_code=201,
    summary="Register a new question",
    description="Endpoint to register a new question with its rubric and related information.",
    tags=["Assessments"],
    responses={
        201: {
            "description": "Question registered successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Question registered successfully",
                        "question_id": "123e4567-e89b-12d3-a456-426614174000",
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
async def register_question(
    request: RegisterQuestionRequest,
    handler: Annotated[RegisterQuestionHandler, Depends(get_register_question_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin", "tutor"]))],
) -> RegisterQuestionResponse:

    response = await handler.handle(request)
    if not response.is_success:
        return RegisterQuestionResponse(
            is_success=False, message=response.message, question_id=None
        )
    return response
