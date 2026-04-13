from typing import Annotated
from fastapi.params import Depends

from src.features.user_management.create_user.create_user_handler import CreateUserHandler
from src.features.user_management.get_user.get_user_handler import GetUserHandler
from src.features.user_management.login.login_handler import LoginHandler
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.token_generator import TokenGenerator
from src.features.user_management.shared.user_repository import UserRepository
from src.infrastructure.database.file_user_repository import FileUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_generator import JWTTokenGenerator


def get_user_repository() -> UserRepository:
    return FileUserRepository(file_path="users.csv")

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()

def get_token_generator() -> TokenGenerator:
    return JWTTokenGenerator()

def get_create_user_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> CreateUserHandler:
    return CreateUserHandler(user_repository, password_hasher)

def get_login_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    token_generator: Annotated[TokenGenerator, Depends(get_token_generator)]
) -> LoginHandler:
    return LoginHandler(user_repository, password_hasher, token_generator)

def get_get_user_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> GetUserHandler:
    return GetUserHandler(user_repository)

