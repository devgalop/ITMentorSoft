from pydantic import BaseModel


class UpdateResourceStatusResponse(BaseModel):
    is_success: bool
    message: str
    content_id: str
    new_status: bool
