from pydantic import BaseModel, field_validator


class UpdateQuestionStatusRequest(BaseModel):
    question_id: str
    status: bool

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError("question_id cannot be empty")
        if len(value) < 5:
            raise ValueError("question_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("question_id must be at most 100 characters long")
        return value

    @field_validator("status")
    def validate_status(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError("status must be a boolean value")
        return value
