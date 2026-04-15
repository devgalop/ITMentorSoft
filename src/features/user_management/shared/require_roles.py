from typing import Annotated, List

from fastapi import HTTPException
from fastapi.params import Depends

from src.features.user_management.shared.get_current_user import get_current_user
from src.features.user_management.shared.token_generator import TokenData

def require_roles(required_roles: List[str]):
    def role_checker(user: Annotated[TokenData, Depends(get_current_user)]):
        if not any(role in user.role for role in required_roles):
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return user
    return role_checker