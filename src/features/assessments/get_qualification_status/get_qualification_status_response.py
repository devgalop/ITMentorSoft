from pydantic import BaseModel


class GetQualificationStatusResponse(BaseModel):
    is_already_qualified: bool
