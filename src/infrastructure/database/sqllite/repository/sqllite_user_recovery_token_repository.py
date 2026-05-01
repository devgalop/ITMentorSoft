from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.user_management.shared.user_recovery_token_repository import (
    RecoveryTokenInfo,
    UserRecoveryTokenRepository,
    UserRecoveryTokenResponse,
)
from src.infrastructure.database.sqllite.models.sqllite_user_recovery_token_mapper import (
    SqlLiteRecoveryTokenMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_user_recovery_token_model import (
    RecoveryTokenEntity,
)


class SqlLiteUserRecoveryTokenRepository(UserRecoveryTokenRepository):

    def __init__(
        self, session_factory: AsyncSession, mapper: Type[SqlLiteRecoveryTokenMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def save_token(self, recovery_token_info: RecoveryTokenInfo):
        entity = self.mapper.to_entity(recovery_token_info)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_user_id_by_transaction_id(
        self, transaction_id: str
    ) -> UserRecoveryTokenResponse | None:
        stmt = select(RecoveryTokenEntity).where(
            RecoveryTokenEntity.id == transaction_id
        )
        result = await self.session_factory.execute(stmt)
        token_found = result.scalars().first()
        if not token_found or token_found.status != "active":
            return None
        return self.mapper.to_model(token_found)

    async def revoke_tokens_by_user_id(self, user_id: str):
        stmt = select(RecoveryTokenEntity).where(RecoveryTokenEntity.user_id == user_id)
        result = await self.session_factory.execute(stmt)
        tokens_to_revoke = result.scalars().all()
        for token in tokens_to_revoke:
            token.status = "revoked"
        await self.session_factory.commit()
