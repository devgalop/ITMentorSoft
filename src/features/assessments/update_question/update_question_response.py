from pydantic import BaseModel


class UpdateQuestionResponse(BaseModel):
    is_success: bool
    message: str
