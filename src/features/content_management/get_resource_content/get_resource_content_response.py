from pydantic import BaseModel

from src.features.content_management.shared.content import ResourceContentResponse


class GetResourceContentResponse(BaseModel):
    is_success: bool
    message: str
    content: ResourceContentResponse | None = None
