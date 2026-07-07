from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_handler import (
    GetAssessmentByTopicHandler,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_request import (
    GetAssessmentByTopicRequest,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_response import (
    GetAssessmentByTopicResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_assessment_by_topic_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/topic",
    status_code=200,
    summary="Get assessment by topic",
    description="Endpoint to generate an assessment for a user based on a specific topic.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Assessment retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Assessment retrieved successfully",
                        "assessment_id": "123e4567e89b12d3a456426614174000",
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
    },
)
async def get_assessment_by_topic(
    topic: str,
    user_id: str,
    number_of_questions: int,
    handler: Annotated[
        GetAssessmentByTopicHandler, Depends(get_get_assessment_by_topic_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["student", "admin"]))],
) -> GetAssessmentByTopicResponse:
    request = GetAssessmentByTopicRequest(
        topic_id=topic, number_of_questions=number_of_questions, student_id=user_id
    )
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.message)
    return response
