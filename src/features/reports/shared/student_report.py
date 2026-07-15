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
    historical_progress: list[StudentProgressDetail]
