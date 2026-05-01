from pydantic import BaseModel, field_validator
import re

USERNAME_PATTERN = r"\w+$"


class GetUserRequest(BaseModel):
    user_id: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Username is required")
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError("Username must be no more than 100 characters long")
        if not re.match(USERNAME_PATTERN, value):
            raise ValueError(
                "Username must be alphanumeric and can include underscores"
            )
        return value
