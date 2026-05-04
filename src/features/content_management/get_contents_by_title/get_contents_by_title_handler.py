from src.features.content_management.get_contents_by_title.get_contents_by_title_request import (
    GetContentsByTitlePaginationRequest,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_response import (
    GetContentsByTitleResponse,
)
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)


class GetContentsByTitleHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentsByTitlePaginationRequest
    ) -> GetContentsByTitleResponse:
        result = await self.content_repository.get_resource_contents_by_title(request)
        return GetContentsByTitleResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=result.items,
            total=result.total,
        )
