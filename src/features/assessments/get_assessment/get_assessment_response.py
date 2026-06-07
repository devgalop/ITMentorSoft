from pydantic import BaseModel


class EvaluativeQuestionData(BaseModel):
    question_id: str
    text_to_evaluate: str


class GetAssessmentResponse(BaseModel):
    is_success: bool
    message: str
    assessment_id: str | None = None
    questions: list[EvaluativeQuestionData] | None = None
