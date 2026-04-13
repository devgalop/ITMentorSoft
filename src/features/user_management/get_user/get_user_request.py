from pydantic import BaseModel, field_validator

class GetUserRequest(BaseModel):
    user_id: str
    
    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("user_id must not be empty")
        return value