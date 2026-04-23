from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.infrastructure.database.sqllite.models.sqllite_permission_model import (
    PermissionEntity,
)
from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base
from src.infrastructure.database.sqllite.models.sqllite_role_permission_model import (
    user_roles,
    role_permissions,
)


class RoleEntity(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)

    users: Mapped[List["UserEntity"]] = relationship(
        "UserEntity", secondary=user_roles, back_populates="roles"
    )
    permissions: Mapped[List["PermissionEntity"]] = relationship(
        "PermissionEntity", secondary=role_permissions, back_populates="roles"
    )
