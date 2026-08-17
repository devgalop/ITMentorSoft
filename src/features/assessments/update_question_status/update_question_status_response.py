from pydantic import BaseModel


class UpdateQuestionStatusResponse(BaseModel):
    is_success: bool
    message: str
    question_id: str
    new_status: bool
