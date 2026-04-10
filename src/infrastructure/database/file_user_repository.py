import aiofiles
from pathlib import Path

from src.features.user_management.shared.user import User, UserRole, UserStatus
from src.features.user_management.shared.user_repository import UserRepository


class FileUserRepository(UserRepository):
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        file_db = Path(file_path)
        file_db.touch(exist_ok=True)
        
    async def save(self, user : User):
        """Save user into file

        Args:
            user (User): The user instance to save.
        """
        async with aiofiles.open(self.file_path, 'a') as f:
            await f.write(f"{user.username},{user.email},{user.password_hashed},{user.status.value},{user.role.value}\n")
    
    async def get_user_by_username(self, username: str) -> User| None:
        """Search user by username field.

        Args:
            username (str): The username of the user to search for.

        Returns:
            User: The user object if found, otherwise None.
        """
        async with aiofiles.open(self.file_path, 'r') as f:
            async for line in f:
                data = line.strip().split(',')
                if data[0] == username:
                    return User(
                        username=data[0],
                        email=data[1],
                        password_hashed=data[2],
                        status=UserStatus(data[3]),
                        role=UserRole(data[4])
                    )
        return None
    
    async def get_user_by_email(self, email: str) -> User| None:
        """Search user by email.

        Args:
            email (str): The email of the user to search for.

        Returns:
            User: The user object if found, otherwise None.
        """
        async with aiofiles.open(self.file_path, 'r') as f:
            async for line in f:
                data = line.strip().split(',')
                if data[1] == email:
                    return User(
                        username=data[0],
                        email=data[1],
                        password_hashed=data[2],
                        status=UserStatus(data[3]),
                        role=UserRole(data[4])
                    )
        return None