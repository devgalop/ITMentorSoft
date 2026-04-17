from typing import Annotated
from fastapi.params import Depends

from src.features.user_management.assign_role.assign_role_handler import (
    AssignRoleHandler,
)
from src.features.user_management.change_password.change_password_handler import (
    ChangePasswordHandler,
)
from src.features.user_management.create_user.create_user_handler import (
    CreateUserHandler,
)

from src.features.user_management.get_available_roles.get_available_roles_handler import (
    GetAvailableRolesHandler,
)
from src.features.user_management.get_user.get_user_handler import GetUserHandler
from src.features.user_management.login.login_handler import LoginHandler
from src.features.user_management.recovery_password.recovery_password_handler import (
    RecoveryPasswordHandler,
)
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.token_generator import TokenGenerator
from src.features.user_management.shared.user_recovery_token_repository import (
    UserRecoveryTokenRepository,
)
from src.features.user_management.shared.user_repository import UserRepository
from src.infrastructure.database.file_user_recovery_token_repository import (
    FileUserRecoveryTokenRepository,
)
from src.infrastructure.database.file_user_repository import FileUserRepository
from src.infrastructure.notification.brevo_notification_service import (
    BrevoNotificationService,
)
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_generator import JWTTokenGenerator
from src.features.shared.notification_service import NotificationService


def get_user_repository() -> UserRepository:
    return FileUserRepository(file_path="db/users.csv")


def get_user_recovery_token_repository() -> UserRecoveryTokenRepository:
    return FileUserRecoveryTokenRepository(file_path="db/recovery_tokens.csv")


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
    token_generator: Annotated[TokenGenerator, Depends(get_token_generator)],
) -> LoginHandler:
    return LoginHandler(user_repository, password_hasher, token_generator)


def get_get_user_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetUserHandler:
    return GetUserHandler(user_repository)


def get_notification_service() -> NotificationService:
    return BrevoNotificationService()


def get_recovery_password_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_recovery_token_repository: Annotated[
        UserRecoveryTokenRepository, Depends(get_user_recovery_token_repository)
    ],
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    token_generator: Annotated[TokenGenerator, Depends(get_token_generator)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> RecoveryPasswordHandler:
    return RecoveryPasswordHandler(
        user_repository,
        user_recovery_token_repository,
        notification_service,
        token_generator,
        password_hasher,
    )


def get_change_password_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_recovery_token_repository: Annotated[
        UserRecoveryTokenRepository, Depends(get_user_recovery_token_repository)
    ],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> ChangePasswordHandler:
    return ChangePasswordHandler(
        user_repository, user_recovery_token_repository, password_hasher
    )


def get_assign_role_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AssignRoleHandler:
    return AssignRoleHandler(user_repository)


def get_get_available_roles_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetAvailableRolesHandler:
    return GetAvailableRolesHandler(user_repository)
