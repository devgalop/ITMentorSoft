from pydantic import BaseModel, field_validator


class GetQuestionByIdRequest(BaseModel):
    question_id: str

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Question ID cannot be empty")
        if len(value) > 32:
            raise ValueError("Question ID cannot be longer than 32 characters")
        if not value.isalnum():
            raise ValueError("Question ID must be alphanumeric")
        return value
