from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.infrastructure.database.sqllite.models.sqllite_role_model import RoleEntity
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base
from src.infrastructure.database.sqllite.models.sqllite_role_permission_model import (
    role_permissions,
)


class PermissionEntity(Base):
    __tablename__ = "permissions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)

    roles: Mapped[List["RoleEntity"]] = relationship(
        "RoleEntity", secondary=role_permissions, back_populates="permissions"
    )
