from pydantic import BaseModel


class StudentKnowledgeProfile(BaseModel):
    topic: str
    score: int

    def get_percentage_score(self) -> float:
        """Calculate the percentage score based on the score value.

        Returns:
            float: The percentage score, calculated as (score / 3) * 100.
        """
        return (self.score / 3) * 100


class StudentSummary(BaseModel):
    student_id: str
    student_name: str
    knowledge_profiles: list[StudentKnowledgeProfile]
    knowledge_classification: str
    feedback: str


class StudentBasicSummary(BaseModel):
    student_id: str
    student_name: str
    knowledge_classification: str


class PaginatedStudentSummary(BaseModel):
    students: list[StudentBasicSummary]
    total_students: int
    page: int


class HistoricalResult(BaseModel):
    topic: str
    score: int
    index: int

    def get_percentage_score(self) -> float:
        """Calculate the percentage score based on the score value.

        Returns:
            float: The percentage score, calculated as (score / 3) * 100.
        """
        return (self.score / 3) * 100


class StudentProgressDetail(BaseModel):
    topic: str
    result: list[HistoricalResult]


class StudentProgress(BaseModel):
    student_id: str
    classification: str
    feedback: str
    historical_progress: list[StudentProgressDetail]


class StudentAnswerScore(BaseModel):
    question_id: str
    question_text: str
    answer: str
    score: float
    feedback: str
    misconceptions: list[str] | None = None
    key_concepts: list[str] | None = None


class StudentAssessmentResult(BaseModel):
    assessment_id: str
    student_id: str
    avg_score: float
    classification: str
    feedback: str
    answer_scores: list[StudentAnswerScore]
