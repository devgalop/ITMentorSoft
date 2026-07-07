from pydantic import BaseModel


class GetQuestionCategoriesResponse(BaseModel):
    is_success: bool
    message: str
    categories: list[str]
