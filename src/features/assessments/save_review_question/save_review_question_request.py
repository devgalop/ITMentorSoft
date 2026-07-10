from pydantic import BaseModel, field_validator


class SaveReviewQuestionRequest(BaseModel):
    question_id: str
    reviewer_id: str
    review_comments: str
    status: str

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError("question_id must not be empty")
        if len(value) < 5:
            raise ValueError("question_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("question_id must not exceed 100 characters")
        return value

    @field_validator("reviewer_id")
    def validate_reviewer_id(cls, value: str) -> str:
        if not value:
            raise ValueError("reviewer_id must not be empty")
        if len(value) < 5:
            raise ValueError("reviewer_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("reviewer_id must not exceed 100 characters")
        return value

    @field_validator("review_comments")
    def validate_review_comments(cls, value: str) -> str:
        if not value:
            raise ValueError("review_comments must not be empty")
        if len(value) < 10:
            raise ValueError("review_comments must be at least 10 characters long")
        if len(value) > 1000:
            raise ValueError("review_comments must not exceed 1000 characters")
        return value

    @field_validator("status")
    def validate_status(cls, value: str) -> str:
        if not value:
            raise ValueError("status must not be empty")
        return value
