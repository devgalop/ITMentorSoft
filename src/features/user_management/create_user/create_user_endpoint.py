from fastapi import APIRouter, Depends
from typing import Annotated

from src.features.user_management.create_user.create_user_handler import CreateUserHandler
from src.features.user_management.create_user.create_user_request import CreateUserRequest
from src.features.user_management.shared.dependencies import get_create_user_handler

router = APIRouter()

@router.post("/")
async def create_user(
    request: CreateUserRequest,
    handler: Annotated[CreateUserHandler, Depends(get_create_user_handler)]
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