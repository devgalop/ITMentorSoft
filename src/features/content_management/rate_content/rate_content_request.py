from pydantic import BaseModel


class RateContent(BaseModel):
    id: str
    content_id: str
    user_id: str
    rating: int
    comment: str | None = None


class RateContentRequest(BaseModel):
    content_id: str
    user_id: str
    rating: int
    comment: str | None = None
