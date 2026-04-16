from src.features.user_management.create_user.create_user_request import (
    CreateUserRequest,
)
from src.features.user_management.create_user.create_user_response import (
    CreateUserResponse,
)
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.user import User, UserRole, UserStatus
from src.features.user_management.shared.user_repository import UserRepository


class CreateUserHandler:
    def __init__(
        self, user_repository: UserRepository, password_hasher: PasswordHasher
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def handle(self, user_data: CreateUserRequest) -> CreateUserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            return CreateUserResponse(is_success=False, message="Email already in use")

        if await self.user_repository.get_user_by_username(user_data.username):
            return CreateUserResponse(
                is_success=False, message="Username already in use"
            )

        password_hashed = self.password_hasher.hash_password(user_data.password)
        user_entity = User(
            username=user_data.username,
            email=user_data.email,
            password_hashed=password_hashed,
            status=UserStatus.ACTIVE,
            role=UserRole.USER,
        )
        await self.user_repository.save(user_entity)

        return CreateUserResponse(
            is_success=True, message="User created successfully", user_id=user_entity.id
        )
