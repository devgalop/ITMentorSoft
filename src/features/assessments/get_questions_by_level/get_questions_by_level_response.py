from pydantic import BaseModel


class EvaluativeQuestionData(BaseModel):
    question_id: str
    text_to_evaluate: str


class GetQuestionsByLevelResponse(BaseModel):
    is_success: bool
    message: str
    questions: list[EvaluativeQuestionData]
