from enum import Enum
import uuid


class UserStatus(Enum):
    """User status

    Args:
        Enum (Enum): Enum class for user status.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserRole(Enum):
    """User role

    Args:
        Enum (Enum): Enum class for user role.
    """

    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User:
    """Represents a system user

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password_hashed (str): The hashed password of the user.
        status (UserStatus): The status of the user.
        role (UserRole): The role of the user.
    """

    def __init__(
        self,
        username: str,
        email: str,
        password_hashed: str,
        status: UserStatus,
        role: UserRole,
    ):
        self.id = uuid.uuid4().hex
        self.username = username
        self.email = email
        self.password_hashed = password_hashed
        self.status = status
        self.role = role

    def is_active(self) -> bool:
        """Validate if the user is active

        Returns:
            bool: True if the user is active, False otherwise.
        """
        return self.status == UserStatus.ACTIVE

    def is_admin(self) -> bool:
        """Validate if the user is an admin

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self.role == UserRole.ADMIN

    def deactivate(self):
        """Deactivate the user"""
        self.status = UserStatus.INACTIVE

    def suspend(self):
        """Suspend the user"""
        self.status = UserStatus.SUSPENDED


class UserResponse:
    """Represents a user response object

    Args:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        status (UserStatus): The status of the user.
        role (UserRole): The role of the user.
    """

    def __init__(
        self, id: str, username: str, email: str, status: UserStatus, role: UserRole
    ):
        self.id = id
        self.username = username
        self.email = email
        self.status = status
        self.role = role
