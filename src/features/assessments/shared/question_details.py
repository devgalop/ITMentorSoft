from pydantic import BaseModel


class RubricScore(BaseModel):
    score: int
    explanation: str


class QuestionDetails(BaseModel):
    question_id: str
    text_to_evaluate: str
    concept: str
    definition: str
    simple_explanation: str
    correct_sample: str
    wrong_sample: str
    common_misconceptions: list[str] = []
    rubric: list[RubricScore] = []
    semantic_keywords: list[str] = []
    status: str
    difficulty: str
    classification: str
    version: int
