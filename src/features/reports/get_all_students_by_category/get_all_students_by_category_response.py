from pydantic import BaseModel


class StudentClassification(BaseModel):
    student_id: str
    student_name: str
    knowledge_classification: str


class PaginatedStudentResult(BaseModel):
    students: list[StudentClassification]
    total_students: int
    page: int


class GetStudentsByCategoryResponse(BaseModel):
    is_success: bool
    message: str
    result: PaginatedStudentResult | None = None
