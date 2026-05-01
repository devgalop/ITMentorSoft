from pydantic import BaseModel


class RegisterContentResponse(BaseModel):
    is_success: bool
    content_id: str | None
    message: str
