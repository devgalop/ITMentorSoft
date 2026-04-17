from abc import ABC, abstractmethod

from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
from src.features.user_management.shared.user import User, UserResponse


class UserRepository(ABC):
    """Interface for user repository implementations.

    Args:
        ABC (ABC): Abstract base class for user repository implementations.
    """

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        """Search user by username field.

        Args:
            username (str): The username of the user to search for.

        Returns:
            User: The user object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Search user by email.

        Args:
            email (str): The email of the user to search for.

        Returns:
            User: The user object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_response_by_email(self, email: str) -> UserResponse | None:
        """Search user by email.

        Args:
            email (str): The email of the user to search for.

        Returns:
            UserResponse: The user response object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> UserResponse | None:
        """Search user by ID.

        Args:
            user_id (str): The ID of the user to search for.

        Returns:
            UserResponse: The user response object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def save(self, user: User):
        """Save changes into database

        Args:
            user (User): The user object to be saved or updated in the database.
        """
        pass

    @abstractmethod
    async def change_password(self, user_id: str, new_password_hashed: str):
        """Change the password of a user.

        Args:
            user_id (str): The ID of the user whose password is to be changed.
            new_password_hashed (str): The new hashed password to be set for the user.
        """
        pass

    @abstractmethod
    async def assign_role_to_user(self, request: AssignRoleRequest):
        """ "Assign a role to a user.

        Args:
            request (AssignRoleRequest): The request object containing user ID and role information.

        """
        pass

    @abstractmethod
    async def get_available_roles(self) -> list[str]:
        """Get the list of available roles.

        Returns:
            list[str]: A list of available roles in the system.
        """
        pass
