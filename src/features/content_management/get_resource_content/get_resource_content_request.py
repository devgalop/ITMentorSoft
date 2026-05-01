from pydantic import BaseModel


class GetResourceRequest(BaseModel):
    content_id: str
