from pydantic import BaseModel, field_validator


class UpdateResourceContentRequest(BaseModel):
    title: str
    description: str
    url: str
    category: str
    related_topic: list[str]

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value:
            raise ValueError("Title must not be empty")
        if len(value) < 5:
            raise ValueError("Title must be at least 5 characters long")
        if len(value) > 150:
            raise ValueError("Title must not exceed 150 characters")
        return value

    @field_validator("description")
    def validate_description(cls, value: str) -> str:
        if not value:
            raise ValueError("Description must not be empty")
        if len(value) < 10:
            raise ValueError("Description must be at least 10 characters long")
        if len(value) > 300:
            raise ValueError("Description must not exceed 300 characters")
        return value

    @field_validator("url")
    def validate_url(cls, value: str) -> str:
        if not value:
            raise ValueError("URL must not be empty")
        if not value.startswith("https://"):
            raise ValueError("Invalid URL format, must start with https://")
        return value
