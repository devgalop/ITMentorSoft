from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base

if TYPE_CHECKING:
    # Imported only for static analysis / type checkers — avoids circular imports at runtime.
    from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity


class RoleEntity(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)

    # One-to-Many: one role can be assigned to many users.
    # The FK lives on UserEntity.role_id — SQLAlchemy resolves the join automatically.
    users: Mapped[List[UserEntity]] = relationship(
        "UserEntity",
        back_populates="role",
    )
