from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base

if TYPE_CHECKING:
    # Imported only for static analysis — avoids a circular import with sqllite_role_model.
    from src.infrastructure.database.sqllite.models.sqllite_role_model import RoleEntity


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    # FK column — nullable so existing rows without a role assignment remain valid.
    role_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("roles.id"), nullable=True, index=True
    )

    # Many-to-One: many users share one role.
    # back_populates mirrors RoleEntity.users (One-to-Many side).
    role: Mapped[Optional[RoleEntity]] = relationship(
        "RoleEntity",
        back_populates="users",
    )
