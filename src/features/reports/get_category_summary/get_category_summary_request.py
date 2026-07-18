from pydantic import BaseModel, field_validator


class GetCategorySummaryRequest(BaseModel):
    category: str

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value:
            raise ValueError("Category must not be empty.")
        if len(value) > 80:
            raise ValueError("Category must not exceed 80 characters.")
        if len(value) < 3:
            raise ValueError("Category must be at least 3 characters long.")
        return value.strip()
