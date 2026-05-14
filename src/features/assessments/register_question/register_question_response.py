from pydantic import BaseModel


class RegisterQuestionResponse(BaseModel):
    is_success: bool
    message: str
    question_id: str | None = None
