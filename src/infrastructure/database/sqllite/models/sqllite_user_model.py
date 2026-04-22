from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
