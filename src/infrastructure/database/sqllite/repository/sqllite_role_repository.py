from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.user_management.shared.role import Role
from src.features.user_management.shared.role_repository import RoleRepository
from src.infrastructure.database.sqllite.models.sqllite_role_mapper import (
    SqlLiteRoleMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_role_model import RoleEntity


class SqlLiteRoleRepository(RoleRepository):

    def __init__(
        self, session_factory: AsyncSession, role_mapper: Type[SqlLiteRoleMapper]
    ):
        self.session_factory = session_factory
        self.role_mapper = role_mapper

    async def get_available_roles(self) -> list[Role]:
        stmt = select(RoleEntity)
        result = await self.session_factory.execute(stmt)
        roles_found = result.scalars().all()
        roles: list[Role] = [self.role_mapper.to_model(role) for role in roles_found]
        return roles

    async def get_role_by_id(self, role_id: str) -> Role | None:
        stmt = select(RoleEntity).where(RoleEntity.id == role_id)
        result = await self.session_factory.execute(stmt)
        role_found = result.scalars().first()
        if not role_found:
            return None
        return self.role_mapper.to_model(role_found)

    async def get_role_by_name(self, name: str) -> Role | None:
        stmt = select(RoleEntity).where(RoleEntity.name == name)
        result = await self.session_factory.execute(stmt)
        role_found = result.scalars().first()
        if not role_found:
            return None
        return self.role_mapper.to_model(role_found)
