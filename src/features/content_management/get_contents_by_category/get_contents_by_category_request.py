from pydantic import BaseModel, field_validator


class GetContentsByCategoryRequest(BaseModel):
    category: str

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Category must not be empty.")
        if len(value) > 100:
            raise ValueError("Category must not exceed 100 characters.")
        if len(value) < 3:
            raise ValueError("Category must be at least 3 characters long.")
        return value.strip()


class GetContentsByCategoryPaginationRequest(GetContentsByCategoryRequest):
    page: int = 0
    page_size: int = 10

    @field_validator("page")
    def validate_page(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Page number must be at least 0.")
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value: int) -> int:
        if value < 1 or value > 100:
            raise ValueError("Page size must be between 1 and 100.")
        return value
