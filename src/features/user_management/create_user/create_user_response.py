from pydantic import BaseModel

class CreateUserResponse(BaseModel):
    is_success: bool
    message: str