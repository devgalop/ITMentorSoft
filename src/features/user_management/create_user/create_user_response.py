from pydantic import BaseModel

class CreateUserResponse(BaseModel):
    is_success: bool
    message: str
    user_id: str | None = None