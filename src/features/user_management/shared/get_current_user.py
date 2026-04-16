from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.features.user_management.shared.dependencies import get_token_generator
from src.features.user_management.shared.token_generator import (
    InvalidTokenError,
    TokenData,
    TokenGenerator,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_generator: TokenGenerator = Depends(get_token_generator),
) -> TokenData:
    try:
        return token_generator.validate_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
