from src.features.content_management.get_resource_content.get_resource_content_request import (
    GetResourceRequest,
)
from src.features.content_management.get_resource_content.get_resource_content_response import (
    GetResourceContentResponse,
)
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)


class GetResourceContentHandler:

    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(self, request: GetResourceRequest) -> GetResourceContentResponse:
        result = await self.content_repository.get_resource_content(request.content_id)

        if result is None:
            return GetResourceContentResponse(
                is_success=False,
                message="Content not found",
                content=None,
            )

        return GetResourceContentResponse(
            is_success=True,
            message="Content retrieved successfully",
            content=result,
        )
