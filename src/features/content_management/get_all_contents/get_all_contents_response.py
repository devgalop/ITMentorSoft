from pydantic import BaseModel

from src.features.content_management.shared.content import ResourceContentResponse


class GetAllContentsResponse(BaseModel):
    is_success: bool
    message: str
    items: list[ResourceContentResponse] = []
    total: int = 0

    model_config = {"arbitrary_types_allowed": True}
