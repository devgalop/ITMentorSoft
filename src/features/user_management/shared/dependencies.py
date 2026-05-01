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
from src.features.user_management.shared.role_repository import RoleRepository
from src.features.user_management.shared.token_generator import TokenGenerator
from src.features.user_management.shared.user_recovery_token_repository import (
    UserRecoveryTokenRepository,
)
from src.features.user_management.shared.user_repository import UserRepository
from src.infrastructure.database.file_user_recovery_token_repository import (
    FileUserRecoveryTokenRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.sqllite.models.sqllite_role_mapper import (
    SqlLiteRoleMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_user_mapper import (
    SqlLiteUserMapper,
)
from src.infrastructure.database.sqllite.repository.sqllite_role_repository import (
    SqlLiteRoleRepository,
)
from src.infrastructure.database.sqllite.repository.sqllite_user_repository import (
    SqlLiteUserRepository,
)
from src.infrastructure.database.sqllite.shared.sqllite_database_session import get_db
from src.infrastructure.notification.brevo_notification_service import (
    BrevoNotificationService,
)
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_token_generator import JWTTokenGenerator
from src.features.shared.notification_service import NotificationService


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return SqlLiteUserRepository(session_factory=session, user_mapper=SqlLiteUserMapper)


def get_role_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> RoleRepository:
    return SqlLiteRoleRepository(session_factory=session, role_mapper=SqlLiteRoleMapper)


def get_user_recovery_token_repository() -> UserRecoveryTokenRepository:
    return FileUserRecoveryTokenRepository(file_path="db/recovery_tokens.csv")


def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def get_token_generator() -> TokenGenerator:
    return JWTTokenGenerator()


def get_create_user_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> CreateUserHandler:
    return CreateUserHandler(user_repository, password_hasher, role_repository)


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
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> AssignRoleHandler:
    return AssignRoleHandler(user_repository, role_repository)


def get_get_available_roles_handler(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> GetAvailableRolesHandler:
    return GetAvailableRolesHandler(role_repository)
