from src.features.user_management.shared.password_hasher import PasswordHasher
import bcrypt


class BcryptPasswordHasher(PasswordHasher):

    def hash_password(self, password: str) -> str:
        """Hashes a password using bcrypt.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: Password hashed using bcrypt.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifies a password against a hashed password using bcrypt.

        Args:
            password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
