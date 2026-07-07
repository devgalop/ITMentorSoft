from pydantic import BaseModel, field_validator


class GetQuestionCategoriesRequest(BaseModel):
    version: int

    @field_validator("version")
    def validate_version(cls, value: int) -> int:
        if value < 1:
            raise ValueError("version must be greater than 0")
        if value > 10:
            raise ValueError("version must be less than or equal to 10")
        return value
