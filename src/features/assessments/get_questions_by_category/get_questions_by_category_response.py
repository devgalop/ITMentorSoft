from pydantic import BaseModel


class QuestionByCategoryData(BaseModel):
    question_id: str
    text_to_evaluate: str


class GetQuestionsByCategoryResponse(BaseModel):
    is_success: bool
    message: str
    questions: list[QuestionByCategoryData]
