from src.features.content_management.get_contents_by_category.get_contents_by_category_request import (
    GetContentsByCategoryPaginationRequest,
)
from src.features.content_management.get_contents_by_category.get_contents_by_category_response import (
    GetContentsByCategoryResponse,
)
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)


class GetContentsByCategoryHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentsByCategoryPaginationRequest
    ) -> GetContentsByCategoryResponse:
        response = await self.content_repository.get_resource_contents_by_category(
            request
        )
        return GetContentsByCategoryResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=response.items,
            total=response.total,
        )
