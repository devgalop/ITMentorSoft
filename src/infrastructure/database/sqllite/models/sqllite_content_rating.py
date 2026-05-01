from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base

if TYPE_CHECKING:
    from src.infrastructure.database.sqllite.models.sqllite_resource_content import (
        ResourceContentEntity,
    )


class ContentRating(Base):
    __tablename__ = "content_ratings"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    content_id: Mapped[str] = mapped_column(String, ForeignKey("contents.id"))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)

    content: Mapped["ResourceContentEntity"] = relationship(
        "ResourceContentEntity",
        back_populates="ratings",
    )
