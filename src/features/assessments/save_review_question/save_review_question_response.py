from pydantic import BaseModel


class SaveReviewQuestionResponse(BaseModel):
    is_success: bool
    message: str
