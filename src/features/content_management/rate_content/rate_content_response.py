from pydantic import BaseModel


class RateContentResponse(BaseModel):
    is_success: bool
    message: str | None = None
