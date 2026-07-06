from pydantic import BaseModel, field_validator


class GetAssessmentByTopicRequest(BaseModel):
    topic_id: str
    number_of_questions: int
    student_id: str

    @field_validator("topic_id")
    def validate_topic_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Topic ID must not be empty")
        if len(value) > 100:
            raise ValueError("Topic ID must not exceed 100 characters")
        if len(value) < 5:
            raise ValueError("Topic ID must be at least 5 characters long")
        return value

    @field_validator("number_of_questions")
    def validate_number_of_questions(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Number of questions must be a positive integer")
        return value

    @field_validator("student_id")
    def validate_student_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Student ID must not be empty")
        if len(value) > 100:
            raise ValueError("Student ID must not exceed 100 characters")
        if len(value) < 5:
            raise ValueError("Student ID must be at least 5 characters long")
        return value
