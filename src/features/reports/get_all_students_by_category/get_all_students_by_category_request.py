from pydantic import BaseModel, field_validator


class GetStudentsByCategoryRequest(BaseModel):
    category: str
    page: int
    page_size: int

    @field_validator("page")
    def validate_page(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Page must be a non-negative integer")
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Page size must be at least 1")
        if value > 100:
            raise ValueError("Page size must not exceed 100")
        return value

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value:
            raise ValueError("Category must not be empty.")
        if len(value) > 80:
            raise ValueError("Category must not exceed 80 characters.")
        if len(value) < 3:
            raise ValueError("Category must be at least 3 characters long.")
        return value
