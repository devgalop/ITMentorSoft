from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.content_management.get_all_contents.get_all_contents_handler import (
    GetAllContentsHandler,
)
from src.features.content_management.get_resource_content.get_resource_content_handler import (
    GetResourceContentHandler,
)
from src.features.content_management.rate_content.rate_content_handler import (
    RateContentHandler,
)
from src.features.content_management.register_content.register_content_handler import (
    RegisterContentHandler,
)
from src.features.content_management.shared.content import ResourceContentBuilder
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)
from src.infrastructure.database.sqllite.models.sqllite_content_rating_mapper import (
    RateContentMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_resource_content_mapper import (
    ResourceContentMapper,
)
from src.infrastructure.database.sqllite.repository.sqllite_resource_content_repository import (
    SqlLiteResourceContentRepository,
)
from src.infrastructure.database.sqllite.shared.sqllite_database_session import get_db


def get_resource_content_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> SqlLiteResourceContentRepository:
    return SqlLiteResourceContentRepository(
        session, ResourceContentMapper, RateContentMapper
    )


def get_register_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> RegisterContentHandler:
    return RegisterContentHandler(content_repository, ResourceContentBuilder)


def get_rate_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> RateContentHandler:
    return RateContentHandler(content_repository)


def get_all_contents_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetAllContentsHandler:
    return GetAllContentsHandler(content_repository)


def get_get_resource_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetResourceContentHandler:
    return GetResourceContentHandler(content_repository)
