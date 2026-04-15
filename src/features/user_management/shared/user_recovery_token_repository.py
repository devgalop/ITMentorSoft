from abc import ABC, abstractmethod
import uuid

class RecoveryTokenInfo:
    """Data class to hold information about a recovery token.

    Args:
        user_id (str): The ID of the user associated with the recovery token.
        token (str): The generated recovery token.
        expiration_time (float): The expiration time of the token in seconds.
        status (str): The status of the token (default is "active").
    """
    def __init__(self, 
                 user_id: str, 
                 token: str, 
                 expiration_time: float, 
                 status: str = "active"):
        self.user_id = user_id
        self.token = token
        self.expiration_time = expiration_time
        self.status = status
        self.id_trx = uuid.uuid4().hex

class UserRecoveryTokenResponse:
    def __init__(self, user_id: str, token_hashed:str, expiration_time:float, status:str):
        self.user_id = user_id
        self.token_hashed = token_hashed
        self.expiration_time = expiration_time
        self.status = status

class UserRecoveryTokenRepository(ABC):
    """ Interface for user recovery token repository implementations.

    Args:
        ABC (ABC): Abstract base class for user recovery token repository implementations.
    """
    
    @abstractmethod
    async def save_token(self, recovery_token_info: RecoveryTokenInfo):
        """Save the generated token along with the associated user ID and expiration time.

        Args:
            recovery_token_info (RecoveryTokenInfo): The information about the recovery token.
        """
        pass
    
    @abstractmethod
    async def get_user_id_by_transaction_id(self, transaction_id: str) -> UserRecoveryTokenResponse | None:
        """Retrieve the user recovery token response associated with a given transaction ID.

        Args:
            transaction_id (str): The transaction ID to search for.

        Returns:
            UserRecoveryTokenResponse: The user recovery token response associated with the transaction ID if found, otherwise None.
        """
        pass
    
    @abstractmethod
    async def revoke_token(self, token: str):
        """Revoke a recovery token from the repository.

        Args:
            token (str): The recovery token to be revoked.
        """
        pass
    
    @abstractmethod
    async def revoke_tokens_by_user_id(self, user_id: str):
        """Revoke all recovery tokens associated with a given user ID.

        Args:
            user_id (str): The ID of the user whose tokens should be revoked.
        """
        pass
