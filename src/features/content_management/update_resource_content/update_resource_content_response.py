from pydantic import BaseModel


class UpdateResourceContentResponse(BaseModel):
    is_success: bool
    message: str
