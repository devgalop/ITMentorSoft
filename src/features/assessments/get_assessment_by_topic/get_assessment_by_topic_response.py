from pydantic import BaseModel


class EvaluativeQuestionDataByTopic(BaseModel):
    question_id: str
    topic: str
    text_to_evaluate: str


class GetAssessmentByTopicResponse(BaseModel):
    is_success: bool
    message: str
    assessment_id: str | None = None
    topic_id: str | None = None
    questions: list[EvaluativeQuestionDataByTopic] | None = None
