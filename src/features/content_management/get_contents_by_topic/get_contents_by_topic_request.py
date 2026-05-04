from pydantic import BaseModel, field_validator


class GetContentsByTopicRequest(BaseModel):
    topic: str

    @field_validator("topic")
    def validate_topic(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Topic must not be empty.")
        if len(value) > 100:
            raise ValueError("Topic must not exceed 100 characters.")
        if len(value) < 3:
            raise ValueError("Topic must be at least 3 characters long.")
        return value.strip()
