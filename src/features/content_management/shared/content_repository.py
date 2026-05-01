from abc import ABC, abstractmethod

from src.features.content_management.rate_content.rate_content_request import (
    RateContent,
)
from src.features.content_management.shared.content import (
    ResourceContent,
    ResourceContentResponse,
)


class ResourceContentRepository(ABC):

    @abstractmethod
    async def save(self, content: ResourceContent):
        """Save educational resource content

        Args:
            content (ResourceContent): The educational resource content to be saved
        """
        pass

    @abstractmethod
    async def get_resource_content(
        self, content_id: str
    ) -> ResourceContentResponse | None:
        """Get educational resource content by content ID
        Args:
            content_id (str): The content ID of the educational resource content to be retrieved
        Returns:
            ResourceContentResponse | None: The educational resource content with the specified content ID, or None if not found
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_category(
        self, category: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by category
        Args:
            category (str): The category of the educational resource contents to be retrieved
        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified category
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_related_topic(
        self, topic: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by related topic
        Args:
            topic (str): The related topic of the educational resource contents to be retrieved
        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified related topic
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_title(
        self, title: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by title
        Args:
            title (str): The title of the educational resource contents to be retrieved
        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified title
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_category_and_related_topic(
        self, category: str, topic: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by category and related topic
        Args:
            category (str): The category of the educational resource contents to be retrieved
            topic (str): The related topic of the educational resource contents to be retrieved
        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified category and related topic
        """
        pass

    @abstractmethod
    async def rate_resource_content(self, request: RateContent):
        """Rate educational resource content
        Args:
            request (RateContent): The request containing the content ID, user ID, rating, and optional comment for rating the educational resource content
        """
        pass
