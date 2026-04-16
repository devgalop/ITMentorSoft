from src.features.user_management.login.login_request import LoginRequest
from src.features.user_management.login.login_response import LoginResponse
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.token_generator import (
    TokenGenerator,
    TokenRequest,
)
from src.features.user_management.shared.user_repository import UserRepository


class LoginHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    async def handle(self, request: LoginRequest) -> LoginResponse:
        """ "Handle the login request.

        Args:
            request (LoginRequest): The login request containing the user's email and password.
        Returns:
            LoginResponse: The response indicating whether the login was successful, along with a token and its expiration time if successful.
        """

        user = await self.user_repository.get_user_by_email(request.email)
        if not user:
            return LoginResponse(
                is_successful=False, token="", expiration_time=0
            )  # nosec

        if not self.password_hasher.verify_password(
            request.password, user.password_hashed
        ):
            return LoginResponse(
                is_successful=False, token="", expiration_time=0
            )  # nosec

        token_response = self.token_generator.generate_token(
            TokenRequest(user_name=user.username, role=user.role.value)
        )

        return LoginResponse(
            is_successful=True,
            token=token_response.token,
            expiration_time=token_response.expiration_time,
        )
