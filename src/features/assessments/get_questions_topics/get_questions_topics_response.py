from pydantic import BaseModel


class GetQuestionsTopicsResponse(BaseModel):
    is_success: bool
    message: str
    topics: list[str]
