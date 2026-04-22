from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
from src.features.user_management.shared.user import User, UserResponse, UserRole
from src.features.user_management.shared.user_repository import UserRepository
from src.infrastructure.database.sqllite.models.sqllite_user_mapper import (
    SqlLiteUserMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity


class SqlLiteUserRepository(UserRepository):

    def __init__(
        self, session_factory: AsyncSession, user_mapper: Type[SqlLiteUserMapper]
    ):
        self.session_factory = session_factory
        self.user_mapper = user_mapper

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(UserEntity).where(UserEntity.username == username)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_model(user_found)

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(UserEntity).where(UserEntity.email == email)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_model(user_found)

    async def get_user_response_by_email(self, email: str) -> UserResponse | None:
        stmt = select(UserEntity).where(UserEntity.email == email)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_response(user_found)

    async def get_user_by_id(self, user_id: str) -> UserResponse | None:
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_response(user_found)

    async def save(self, user: User):
        user_entity = self.user_mapper.to_entity(user)
        self.session_factory.add(user_entity)
        await self.session_factory.commit()

    async def change_password(self, user_id: str, new_password_hashed: str):
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        user_found.hashed_password = new_password_hashed
        await self.session_factory.commit()

    async def assign_role_to_user(self, request: AssignRoleRequest):
        stmt = select(UserEntity).where(UserEntity.id == request.user_id)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        user_found.role = request.role
        await self.session_factory.commit()

    async def get_available_roles(self) -> list[str]:
        return [role.value for role in UserRole]
