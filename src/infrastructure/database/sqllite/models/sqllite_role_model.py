from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class RoleEntity(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)
