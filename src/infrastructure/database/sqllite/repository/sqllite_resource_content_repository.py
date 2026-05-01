from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.content_management.rate_content.rate_content_request import (
    RateContent,
)
from src.features.content_management.shared.content import (
    ResourceContent,
    ResourceContentResponse,
)
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)
from src.infrastructure.database.sqllite.models.sqllite_content_rating_mapper import (
    RateContentMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_resource_content import (
    ResourceContentEntity,
)
from src.infrastructure.database.sqllite.models.sqllite_resource_content_mapper import (
    ResourceContentMapper,
)


class SqlLiteResourceContentRepository(ResourceContentRepository):

    def __init__(
        self,
        session_factory: AsyncSession,
        mapper: Type[ResourceContentMapper],
        rating_mapper: Type[RateContentMapper],
    ):
        self.session_factory = session_factory
        self.mapper = mapper
        self.rating_mapper = rating_mapper

    async def save(self, content: ResourceContent):
        entity = self.mapper.to_entity(content)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_resource_content(
        self, content_id: str
    ) -> ResourceContentResponse | None:
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.id == content_id
        )
        result = await self.session_factory.execute(smt)
        content_entity = result.scalars().first()
        if not content_entity:
            return None
        return self.mapper.to_model(content_entity)

    async def get_resource_contents_by_category(
        self, category: str
    ) -> list[ResourceContentResponse]:
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.category == category
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return [self.mapper.to_model(entity) for entity in content_entities]

    async def get_resource_contents_by_related_topic(
        self, topic: str
    ) -> list[ResourceContentResponse]:
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.related_topics.like(f"%{topic}%")
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return [self.mapper.to_model(entity) for entity in content_entities]

    async def get_resource_contents_by_title(
        self, title: str
    ) -> list[ResourceContentResponse]:
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.title.like(f"%{title}%")
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return [self.mapper.to_model(entity) for entity in content_entities]

    async def get_resource_contents_by_category_and_related_topic(
        self, category: str, topic: str
    ) -> list[ResourceContentResponse]:
        smt = (
            select(ResourceContentEntity)
            .where(ResourceContentEntity.category == category)
            .where(ResourceContentEntity.related_topics.like(f"%{topic}%"))
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return [self.mapper.to_model(entity) for entity in content_entities]

    async def rate_resource_content(self, request: RateContent):
        entity = self.rating_mapper.to_entity(request)
        self.session_factory.add(entity)
        await self.session_factory.commit()
