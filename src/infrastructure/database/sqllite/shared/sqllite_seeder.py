from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy import select
import os
from dotenv import load_dotenv
from src.features.user_management.shared.dependencies import get_password_hasher
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.infrastructure.database.sqllite.models.sqllite_role_model import RoleEntity
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
        result = await session.execute(select(RoleEntity))
        roles = result.scalars().all()

        if roles:
            print("Database already seeded. Skipping seeding.")
            return

        role_admin = RoleEntity(
            id=uuid.uuid4().hex,
            name="admin",
            description="Administrator role with full permissions.",
        )
        session.add(role_admin)
        role_teacher = RoleEntity(
            id=uuid.uuid4().hex,
            name="teacher",
            description="Teacher role with permissions to manage courses and students.",
        )
        session.add(role_teacher)
        role_student = RoleEntity(
            id=uuid.uuid4().hex,
            name="student",
            description="Student role with permissions to access course materials.",
        )
        session.add(role_student)
        role_user = RoleEntity(
            id=uuid.uuid4().hex,
            name="user",
            description="Default user role with limited permissions.",
        )
        session.add(role_user)
        await session.commit()

        admin = UserEntity(
            id=uuid.uuid4().hex,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            hashed_password=password_hasher.hash_password(ADMIN_PASSWORD),
            status="active",
            role_id=role_admin.id,
        )
        session.add(admin)
        await session.commit()
        print("Admin user created")
