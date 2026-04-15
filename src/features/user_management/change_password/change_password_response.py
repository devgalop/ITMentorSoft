from pydantic import BaseModel

class ChangePasswordResponse(BaseModel):
    is_success: bool
    message: str