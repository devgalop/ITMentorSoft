from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.shared.dependencies import (
    get_update_resource_content_handler,
)
from src.features.content_management.update_resource_content.update_resource_content_handler import (
    UpdateResourceContentHandler,
)
from src.features.content_management.update_resource_content.update_resource_content_request import (
    UpdateResourceContentRequest,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.put(
    "/{content_id}",
    status_code=200,
    summary="Update educational resource content",
    description="Endpoint to update educational resource content in the system.",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Content updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Content with ID {content_id} has been successfully updated.",
                    }
                }
            },
        },
        400: {
            "description": "Bad Request. Content update failed due to invalid input data or content with the specified ID does not exist.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Content update failed. Invalid input data or content with the specified ID does not exist.",
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized. Content update failed due to missing or invalid authentication.",
            "content": {"application/json": {"example": {"message": "Unauthorized."}}},
        },
    },
)
async def update_resource_content(
    content_id: str,
    request: UpdateResourceContentRequest,
    handler: Annotated[
        UpdateResourceContentHandler, Depends(get_update_resource_content_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
):
    if not content_id:
        raise HTTPException(status_code=400, detail="Content ID is required.")

    response = await handler.handle(content_id, request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())

    return response
