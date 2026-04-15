from fastapi import APIRouter, Depends
from typing import Annotated

from src.features.user_management.change_password.change_password_handler import ChangePasswordHandler
from src.features.user_management.change_password.change_password_request import ChangePasswordRequestWithToken, ChangePasswordRequest
from src.features.user_management.change_password.change_password_response import ChangePasswordResponse
from src.features.user_management.shared.dependencies import get_change_password_handler

router = APIRouter()

@router.put("/change-password",
             status_code=200,
             summary="Change user password using a recovery token",
             description="Changes the user's password using a valid recovery token. The token is sent to the user's email during the password recovery process.",
             tags=["User Management"],
             responses={
                 200: {
                     "description": "Password changed successfully. Returns a message indicating the successful password change.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "is_success": True,
                                 "message": "Password changed successfully."
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Bad Request. Password change failed due to invalid token or user not found.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "is_success": False,
                                 "message": "Invalid or expired token"
                             }
                         }
                     }
                 }
             })
async def change_password(
    token: str,
    id_trx: str,
    request: ChangePasswordRequest,
    handler: Annotated[ChangePasswordHandler, Depends(get_change_password_handler)]
)-> ChangePasswordResponse:
    """Changes the user's password using a valid recovery token.

    Args:
        token (str): The recovery token sent to the user's email.
        id_trx (str): The transaction ID associated with the password recovery request.
        request (ChangePasswordRequest): The new password for the user.
        handler (Annotated[ChangePasswordHandler, Depends]): The handler responsible for processing the password change.

    Returns:
        ChangePasswordResponse: A response indicating the result of the password change operation.
    """
    if not token:
        return ChangePasswordResponse(is_success=False, message="Token is required")

    if not id_trx:
        return ChangePasswordResponse(is_success=False, message="Transaction ID is required")
    
    change_password_request = ChangePasswordRequestWithToken(token=token, id_trx=id_trx, new_password=request.new_password)
    response = await handler.handle(change_password_request)
    return response
    

