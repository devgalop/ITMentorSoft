from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.reports.get_student_progress.get_student_progress_handler import (
    GetStudentProgressHandler,
)
from src.features.reports.get_student_progress.get_student_progress_request import (
    GetStudentProgressRequest,
)
from src.features.reports.shared.dependencies import get_get_student_progress_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/student_progress",
    status_code=200,
    summary="Get student progress",
    description="Endpoint to retrieve the student progress for a given user ID.",
    tags=["Reports"],
    responses={
        200: {
            "description": "Student progress retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Student progress retrieved successfully",
                        "progress": {
                            "student_id": "123e4567e89b12d3a456426614174000",
                            "classification": "Intermediate",
                            "knowledge_profile": [
                                {"topic": "Mathematics", "score": 85.0, "index": 1}
                            ],
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
async def get_student_progress(
    id: str,
    handler: Annotated[
        GetStudentProgressHandler, Depends(get_get_student_progress_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher", "student"]))],
):
    """Endpoint to retrieve the student progress for a given user ID.

    Args:
        id (str): The user ID of the student.
        handler (GetStudentProgressHandler): The handler to process the request.
        _ (TokenData): The token data for authentication and authorization.

    Returns:
        GetStudentProgressResponse: The response containing the student progress.
    """
    request = GetStudentProgressRequest(student_id=id)
    response = await handler.handle(request)

    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.message)

    return response
