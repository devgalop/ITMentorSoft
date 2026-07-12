from pydantic import BaseModel


class KnowledgeProfile(BaseModel):
    topic: str
    score: float


class SummaryResponse(BaseModel):
    student_id: str
    name: str
    knowledge_classification: str
    profile: list[KnowledgeProfile]
    feedback: str


class GetStudentSummaryResponse(BaseModel):
    is_success: bool
    message: str
    summary: SummaryResponse | None = None
