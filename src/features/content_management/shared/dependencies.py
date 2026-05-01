from typing import Annotated
from fastapi import Depends

from src.features.content_management.register_content.register_content_handler import (
    RegisterContentHandler,
)
from src.features.content_management.shared.content import ResourceContentBuilder
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)
from src.infrastructure.database.file_resource_content_repository import (
    FileResourceContentRepository,
)


def get_resource_content_repository() -> ResourceContentRepository:
    return FileResourceContentRepository(file_path="db/content.csv")


def get_register_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> RegisterContentHandler:
    return RegisterContentHandler(content_repository, ResourceContentBuilder)
