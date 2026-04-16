from fastapi import APIRouter, Depends
from typing import Annotated

from src.features.user_management.create_user.create_user_handler import (
    CreateUserHandler,
)
from src.features.user_management.create_user.create_user_request import (
    CreateUserRequest,
)
from src.features.user_management.shared.dependencies import get_create_user_handler

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    summary="Create User",
    description="Endpoint for creating a new user. Returns a message indicating the result of the user creation.",
    tags=["User Management"],
    responses={
        201: {
            "description": "User created successfully. Returns a message indicating the successful creation.",
            "content": {
                "application/json": {
                    "example": {"message": "User created successfully."}
                }
            },
        },
        400: {
            "description": "Bad Request. User creation failed due to invalid input data.",
            "content": {
                "application/json": {
                    "example": {"message": "User creation failed. Invalid input data."}
                }
            },
        },
    },
)
async def create_user(
    request: CreateUserRequest,
    handler: Annotated[CreateUserHandler, Depends(get_create_user_handler)],
):
    """Endpoint for creating a new user.

    Args:
        request (CreateUserRequest): The user data for creating a new user.
        handler (Annotated[CreateUserHandler, Depends]): The handler responsible for processing the user creation.

    Returns:
        dict: A dictionary containing the message about the user creation result.
    """
    response = await handler.handle(request)
    return {"message": response.message}
