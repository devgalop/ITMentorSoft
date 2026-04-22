from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy import select
import os
from dotenv import load_dotenv
from src.features.user_management.shared.dependencies import get_password_hasher
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.infrastructure.database.sqllite.shared.sqllite_database_session import (
    AsyncSessionLocal,
)
from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity

load_dotenv()

ADMIN_USERNAME: str = os.getenv("DATABASE_ADMIN_USERNAME", "")
ADMIN_PASSWORD: str = os.getenv("DATABASE_ADMIN_PASSWORD", "")
ADMIN_EMAIL: str = os.getenv("DATABASE_ADMIN_EMAIL", "")


async def seed_database(
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserEntity))
        users = result.scalars().all()

        if users:
            print("Database already seeded. Skipping seeding.")
            return

        admin = UserEntity(
            id=uuid.uuid4().hex,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            hashed_password=password_hasher.hash_password(ADMIN_PASSWORD),
            status="active",
            role="admin",
        )
        session.add(admin)
        await session.commit()
        print("Admin user created")
