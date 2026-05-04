from src.features.content_management.get_contents_by_topic.get_contents_by_topic_request import (
    GetContentsByTopicRequest,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_response import (
    GetContentsByTopicResponse,
)
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)


class GetContentsByTopicHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentsByTopicRequest
    ) -> GetContentsByTopicResponse:

        result = await self.content_repository.get_resource_contents_by_related_topic(
            request.topic
        )
        return GetContentsByTopicResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=result,
            total=result.__len__(),
        )
