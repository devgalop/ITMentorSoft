from pydantic import BaseModel

from src.features.content_management.shared.content import ResourceContentResponse


class GetContentsByCategoryResponse(BaseModel):
    is_success: bool
    message: str
    items: list[ResourceContentResponse] = []
    total: int = 0
