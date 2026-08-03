from pydantic import BaseModel


class CreateUserFromAdminResponse(BaseModel):
    is_success: bool
    message: str
    user_id: str | None = None
