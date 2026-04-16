from pydantic import BaseModel, field_validator
import re

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*()_+\-=\[\]{}|;\'":,.<>\/?]'


class RecoveryPasswordRequest(BaseModel):
    email: str

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        if not value:
            raise ValueError("Email is required")
        if len(value) < 5:
            raise ValueError("Email must be at least 5 characters long")
        if len(value) > 255:
            raise ValueError("Email must be no more than 255 characters long")
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError("Invalid email format")
        return value
