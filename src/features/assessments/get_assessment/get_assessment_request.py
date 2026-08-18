from pydantic import BaseModel, field_validator


class GetAssessmentRequest(BaseModel):
    student_id: str

    @field_validator("student_id")
    def validate_student_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Student ID must not be empty")
        if len(value) > 100:
            raise ValueError("Student ID must not exceed 100 characters")
        if len(value) < 5:
            raise ValueError("Student ID must be at least 5 characters long")
        return value
