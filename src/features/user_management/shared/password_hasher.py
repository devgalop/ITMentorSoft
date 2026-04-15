from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    """ Interface for password hashing and verification.

    Args:
        ABC (_type_): Abstract base class for password hashing
    """
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a password.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password.
        
        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        pass