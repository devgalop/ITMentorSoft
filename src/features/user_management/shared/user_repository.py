from abc import ABC, abstractmethod

from src.features.user_management.shared.user import User, UserResponse

class UserRepository(ABC):
    """ Interface for user repository implementations.

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