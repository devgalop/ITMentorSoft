from pydantic import BaseModel

from src.features.assessments.shared.question_details import QuestionDetails


class GetPendingApprovalQuestionsResponse(BaseModel):
    is_success: bool
    message: str
    questions: list[QuestionDetails] = []
    total: int = 0
