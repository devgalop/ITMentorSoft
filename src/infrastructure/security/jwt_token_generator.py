import os
import jwt
from datetime import datetime, timedelta, timezone 
from dotenv import load_dotenv

from src.features.user_management.shared.token_generator import InvalidTokenError, TokenData, TokenGenerator, TokenRequest, TokenResponse
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_DELTA_SECONDS = os.getenv("JWT_EXPIRATION_DELTA_SECONDS", "300")  # Default to 5 minutes if not set

class TokenPayload:
    def __init__(self, user_name: str, role: str, exp: datetime):
        self.user_name = user_name
        self.role = role
        self.exp = exp
        
    def to_dict(self) -> dict[str, str | datetime]:
        return {
            "user_name": self.user_name,
            "role": self.role,
            "exp": self.exp
        }

class JWTTokenGenerator(TokenGenerator):
    
    def generate_token(self, request: TokenRequest) -> TokenResponse:
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(seconds=int(JWT_EXPIRATION_DELTA_SECONDS))
        token_payload = TokenPayload(
            user_name=request.user_name,
            role=request.role,
            exp=expiration_time
        ).to_dict()
        return TokenResponse(
            token=jwt.encode(token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM), # pyright: ignore[reportUnknownMemberType]
            expiration_time=expiration_time.timestamp()
        )
    
    def validate_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM) # pyright: ignore[reportUnknownMemberType]
            if(datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(tz=timezone.utc)):
                raise jwt.ExpiredSignatureError("Expired token")
            return TokenData(
                user_name=payload["user_name"],
                role=payload["role"]
            )
        except jwt.PyJWTError as e:
            raise InvalidTokenError(str(e)) from e