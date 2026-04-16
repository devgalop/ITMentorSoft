from fastapi import APIRouter, Depends
from typing import Annotated

from src.features.user_management.recovery_password.recovery_password_handler import (
    RecoveryPasswordHandler,
)
from src.features.user_management.recovery_password.recovery_password_request import (
    RecoveryPasswordRequest,
)
from src.features.user_management.recovery_password.recovery_password_response import (
    RecoveryPasswordResponse,
)
from src.features.user_management.shared.dependencies import (
    get_recovery_password_handler,
)

router = APIRouter()


@router.post(
    "/recovery-password",
    status_code=200,
    summary="Recovery Password",
    description="Endpoint for initiating the password recovery process. Accepts the user's email and sends a password recovery email if the email exists in the system. Always returns a success message to prevent email enumeration.",
    tags=["User Management"],
    responses={
        200: {
            "description": "Password recovery initiated. Always returns a success message to prevent email enumeration.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "If the email exists in our system, you will receive a password recovery email shortly."
                    }
                }
            },
        },
        400: {
            "description": "Bad Request. Returns an error message if the request is invalid.",
            "content": {
                "application/json": {"example": {"detail": "Invalid email format"}}
            },
        },
    },
)
async def recovery_password(
    request: RecoveryPasswordRequest,
    handler: Annotated[RecoveryPasswordHandler, Depends(get_recovery_password_handler)],
) -> RecoveryPasswordResponse:
    """Endpoint for initiating the password recovery process.

    Args:
        request (RecoveryPasswordRequest): The request containing the user's email for password recovery.
        handler (Annotated[RecoveryPasswordHandler, Depends]): The handler responsible for processing the password recovery request.
    Returns:
        RecoveryPasswordResponse: The response containing a message indicating that the password recovery process has been initiated. Always returns a success message to prevent email enumeration.
    """
    response = await handler.handle(request)
    return response
