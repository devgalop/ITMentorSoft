from pydantic import BaseModel


class AnswerScore(BaseModel):
    question_id: str
    question_text: str
    answer: str
    score: float
    feedback: str
    misconceptions: list[str] | None = None
    key_concepts: list[str] | None = None


class StudentAssessmentResult(BaseModel):
    assessment_id: str
    user_id: str
    avg_score: float
    classification: str
    feedback: str
    answer_scores: list[AnswerScore]


class GetAssessmentResultResponse(BaseModel):
    is_success: bool
    message: str
    result: StudentAssessmentResult | None = None
