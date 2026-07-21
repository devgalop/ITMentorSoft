from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.reports.get_all_students.get_all_students_handler import (
    GetAllStudentsHandler,
)
from src.features.reports.get_all_students.get_all_students_request import (
    GetAllStudentsRequest,
)
from src.features.reports.get_all_students.get_all_students_response import (
    GetAllStudentsResponse,
)
from src.features.reports.shared.dependencies import get_get_all_students_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/students",
    status_code=200,
    summary="Get all students",
    description="Retrieve a paginated list of all students.",
    tags=["Reports"],
    responses={
        200: {
            "description": "Students retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Students retrieved successfully",
                        "students": [
                            {
                                "user_id": 1,
                                "name": "John Doe",
                                "email": "john.doe@example.com",
                            }
                        ],
                        "total_students": 100,
                        "page": 1,
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
            "description": "Students not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Students not found"}
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
async def get_all_students(
    page: int,
    page_size: int,
    handler: Annotated[GetAllStudentsHandler, Depends(get_get_all_students_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetAllStudentsResponse:
    """Endpoint to retrieve a paginated list of all students.

    Args:
        page (int): The page number to retrieve.
        page_size (int): The number of students per page.
        handler (GetAllStudentsHandler): The handler to process the request.
        _: TokenData: The token data for authentication and authorization.

    Returns:
        GetAllStudentsResponse: The response containing the list of students.
    """

    request = GetAllStudentsRequest(page=page, page_size=page_size)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.message)
    return response
