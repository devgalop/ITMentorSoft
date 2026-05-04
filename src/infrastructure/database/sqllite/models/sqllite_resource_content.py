from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.infrastructure.database.sqllite.models.sqllite_content_rating import (
    ContentRating,
)
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class ResourceContentEntity(Base):
    __tablename__ = "contents"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    summary: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    related_topics: Mapped[str] = mapped_column(
        String
    )  # Store as comma-separated string

    ratings: Mapped[List[ContentRating]] = relationship(
        "ContentRating",
        back_populates="content",
        cascade="all, delete-orphan",
    )
