from pydantic import BaseModel, field_validator


class GetQualificationStatusRequest(BaseModel):
    user_id: str
    assessment_id: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("user_id must not be empty")
        if len(value) < 5:
            raise ValueError("user_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("user_id must not exceed 100 characters")
        return value

    @field_validator("assessment_id")
    def validate_assessment_id(cls, value: str) -> str:
        if not value:
            raise ValueError("assessment_id must not be empty")
        if len(value) < 5:
            raise ValueError("assessment_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("assessment_id must not exceed 100 characters")
        return value
