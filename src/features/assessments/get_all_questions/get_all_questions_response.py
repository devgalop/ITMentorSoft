from pydantic import BaseModel

from src.features.assessments.shared.question import QuestionDetails


class GetAllQuestionsResponse(BaseModel):
    is_success: bool
    message: str
    items: list[QuestionDetails] = []
    total: int = 0
