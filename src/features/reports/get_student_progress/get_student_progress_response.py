from pydantic import BaseModel


class KnowledgeProfile(BaseModel):
    topic: str
    score: float
    index: int


class ProgressResponse(BaseModel):
    student_id: str
    classification: str
    knowledge_profile: list[KnowledgeProfile]


class GetStudentProgressResponse(BaseModel):
    is_success: bool
    message: str
    progress: ProgressResponse | None
