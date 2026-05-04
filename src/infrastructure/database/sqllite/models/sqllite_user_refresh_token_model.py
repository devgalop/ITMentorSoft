from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class RefreshTokenEntity(Base):
    __tablename__ = "user_refresh_tokens"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    expiration_time: Mapped[float] = mapped_column()
    status: Mapped[str] = mapped_column(String)

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
