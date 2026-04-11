from abc import ABC, abstractmethod

class TokenRequest:
    """Data class for token generation request.
    Args:
        user_name (str): The username for which the token is being generated.
        role (str): The role of the user (e.g., "student", "teacher").
    """
    def __init__(self, user_name: str, role: str):
        self.user_name = user_name
        self.role = role
        
class TokenResponse:
    """Data class for token generation response.
    Args:
        token (str): The generated token.
        expiration_time (float): The time in seconds until the token expires. unix timestamp format.
    """
    def __init__(self, token: str, expiration_time: float):
        self.token = token
        self.expiration_time = expiration_time
        

class TokenGenerator(ABC):
    """ Interface for token generation and validation.

    Args:
        ABC (_type_): Abstract base class for token generation
    """
    
    @abstractmethod
    def generate_token(self, request: TokenRequest) -> TokenResponse:
        """Generate a token based on the provided request.

        Args:
            request (TokenRequest): The token generation request containing user information and expiration time.

        Returns:
            TokenResponse: The generated token and its expiration time.
        """
        pass