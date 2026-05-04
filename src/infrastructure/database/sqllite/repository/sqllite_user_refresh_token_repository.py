from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.user_management.shared.refresh_token_repository import (
    RefreshTokenData,
    RefreshTokenInfo,
    RefreshTokenRepository,
)
from src.infrastructure.database.sqllite.models.sqllite_user_refresh_token_mapper import (
    SqlLiteRefreshTokenMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_user_refresh_token_model import (
    RefreshTokenEntity,
)


class SqlLiteUserRefreshTokenRepository(RefreshTokenRepository):

    def __init__(
        self, session_factory: AsyncSession, mapper: Type[SqlLiteRefreshTokenMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def save_token(self, info: RefreshTokenInfo):
        entity = self.mapper.to_entity(info)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_active_token(self, user_id: str) -> RefreshTokenData | None:
        stmt = select(RefreshTokenEntity).where(
            RefreshTokenEntity.status == "active", RefreshTokenEntity.user_id == user_id
        )
        result = await self.session_factory.execute(stmt)
        active_token = result.scalars().first()

        if not active_token:
            return None

        return self.mapper.to_model(active_token)

    async def revoke_tokens_by_user_id(self, user_id: str):
        stmt = select(RefreshTokenEntity).where(RefreshTokenEntity.user_id == user_id)
        result = await self.session_factory.execute(stmt)
        tokens_to_revoke = result.scalars().all()
        for token in tokens_to_revoke:
            token.status = "revoked"
        await self.session_factory.commit()
