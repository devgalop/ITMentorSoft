

from typing import Annotated

from fastapi.params import Depends

from src.features.user_management.create_user.create_user_handler import CreateUserHandler
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.user_repository import UserRepository
from src.infrastructure.database.file_user_repository import FileUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher


def get_user_repository() -> UserRepository:
    return FileUserRepository(file_path="users.csv")

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()

def get_create_user_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> CreateUserHandler:
    return CreateUserHandler(user_repository, password_hasher)