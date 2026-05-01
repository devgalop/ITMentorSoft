import aiofiles
from pathlib import Path

from src.features.content_management.shared.content import (
    ContentCategory,
    ResourceContent,
    ResourceContentResponse,
)
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)


class FileResourceContentRepository(ResourceContentRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path
        file_db = Path(file_path)
        file_db.touch(exist_ok=True)

    async def save(self, content: ResourceContent):
        """Save educational resource content into file.

        Args:
            content (ResourceContent): The educational resource to be saved.
        """
        related_topics = "|".join(map(str, content.related_topics))
        async with aiofiles.open(self.file_path, mode="a") as f:
            await f.write(
                f"{content.content_id},{content.title},{content.summary},{content.url},{content.category.value},{related_topics}\n"
            )

    async def get_resource_content(
        self, content_id: str
    ) -> ResourceContentResponse | None:
        """Get educational resource content by content ID.

        Args:
            content_id (str): The content ID of the educational resource content to be retrieved.

        Returns:
            ResourceContentResponse | None: The educational resource content with the specified content ID, or None if not found.
        """
        async with aiofiles.open(self.file_path, mode="r") as f:
            async for line in f:
                data = line.strip().split(",")
                if data[0] == content_id:
                    return ResourceContentResponse(
                        content_id=data[0],
                        title=data[1],
                        summary=data[2],
                        url=data[3],
                        category=ContentCategory(data[4]),
                        related_topics=self._parse_topics(data[5]),
                    )
        return None

    async def get_resource_contents_by_category(
        self, category: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by category.

        Args:
            category (str): The category of the educational resource contents to be retrieved.

        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified category.
        """
        contents: list[ResourceContentResponse] = []
        async with aiofiles.open(self.file_path, mode="r") as f:
            async for line in f:
                data = line.strip().split(",")
                if data[4] == category:
                    contents.append(
                        ResourceContentResponse(
                            content_id=data[0],
                            title=data[1],
                            summary=data[2],
                            url=data[3],
                            category=ContentCategory(data[4]),
                            related_topics=self._parse_topics(data[5]),
                        )
                    )
        return contents

    async def get_resource_contents_by_related_topic(
        self, topic: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by related topic.

        Args:
            topic (str): The related topic of the educational resource contents to be retrieved.

        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified related topic.
        """
        contents: list[ResourceContentResponse] = []
        async with aiofiles.open(self.file_path, mode="r") as f:
            async for line in f:
                data = line.strip().split(",")
                related_topics = self._parse_topics(data[5])
                if topic in related_topics:
                    contents.append(
                        ResourceContentResponse(
                            content_id=data[0],
                            title=data[1],
                            summary=data[2],
                            url=data[3],
                            category=ContentCategory(data[4]),
                            related_topics=related_topics,
                        )
                    )
        return contents

    async def get_resource_contents_by_title(
        self, title: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by title.

        Args:
            title (str): The title of the educational resource contents to be retrieved.

        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified title.
        """
        contents: list[ResourceContentResponse] = []
        async with aiofiles.open(self.file_path, mode="r") as f:
            async for line in f:
                data = line.strip().split(",")
                if data[1] == title:
                    contents.append(
                        ResourceContentResponse(
                            content_id=data[0],
                            title=data[1],
                            summary=data[2],
                            url=data[3],
                            category=ContentCategory(data[4]),
                            related_topics=self._parse_topics(data[5]),
                        )
                    )
        return contents

    async def get_resource_contents_by_category_and_related_topic(
        self, category: str, topic: str
    ) -> list[ResourceContentResponse]:
        """Get educational resource contents by category and related topic.

        Args:
            category (str): The category of the educational resource contents to be retrieved.
            topic (str): The related topic of the educational resource contents to be retrieved.
        Returns:
            list[ResourceContentResponse]: A list of educational resource contents with the specified category and related topic.
        """
        contents: list[ResourceContentResponse] = []
        async with aiofiles.open(self.file_path, mode="r") as f:
            async for line in f:
                data = line.strip().split(",")
                related_topics = self._parse_topics(data[5])
                if data[4] == category and topic in related_topics:
                    contents.append(
                        ResourceContentResponse(
                            content_id=data[0],
                            title=data[1],
                            summary=data[2],
                            url=data[3],
                            category=ContentCategory(data[4]),
                            related_topics=related_topics,
                        )
                    )
        return contents

    def _parse_topics(self, topics_str: str) -> list[str]:
        """Parse related topics from a string.

        Args:
            topics_str (str): The string containing related topics separated by '|'.
        Returns:
            list[str]: A list of related topics.
        """
        if not topics_str:
            return []
        return topics_str.split("|")
