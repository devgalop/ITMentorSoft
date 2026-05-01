from src.features.user_management.shared.user import (
    User,
    UserRole,
    UserStatus,
    UserResponse,
)
from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity


class SqlLiteUserMapper:

    @staticmethod
    def to_entity(user_model: User) -> UserEntity:
        """Map user domain model into user entity

        Args:
            user_model (User): User domain model

        Returns:
            UserEntity: User entity
        """
        return UserEntity(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.password_hashed,
            status=user_model.status.value,
            role=user_model.role.value,
        )

    @staticmethod
    def to_model(user_entity: UserEntity) -> User:
        """Map user entity into user domain model
        Args:
            user_entity (UserEntity): User entity
        Returns:
            User: User domain model
        """
        return User(
            username=user_entity.username,
            email=user_entity.email,
            password_hashed=user_entity.hashed_password,
            status=UserStatus(user_entity.status),
            role=UserRole(user_entity.role),
        )

    @staticmethod
    def to_response(user_entity: UserEntity) -> UserResponse:
        """Map user entity into user response
        Args:
            user_entity (UserEntity): User entity
        Returns:
            UserResponse: User response
        """
        return UserResponse(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            status=UserStatus(user_entity.status),
            role=UserRole(user_entity.role),
        )
