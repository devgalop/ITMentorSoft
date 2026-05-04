from src.features.content_management.shared.content import (
    ContentCategory,
    ResourceContent,
    ResourceContentResponse,
)
from src.infrastructure.database.sqllite.models.sqllite_resource_content import (
    ResourceContentEntity,
)


class ResourceContentMapper:

    @staticmethod
    def to_entity(content: ResourceContent) -> ResourceContentEntity:
        return ResourceContentEntity(
            id=content.content_id,
            title=content.title,
            summary=content.summary,
            url=content.url,
            category=content.category.value,
            related_topics="|".join(content.related_topics),
        )

    @staticmethod
    def to_model(entity: ResourceContentEntity) -> ResourceContentResponse:
        return ResourceContentResponse(
            content_id=entity.id,
            title=entity.title,
            summary=entity.summary,
            url=entity.url,
            category=ContentCategory(entity.category),
            related_topics=(
                entity.related_topics.split("|") if entity.related_topics else []
            ),
        )
