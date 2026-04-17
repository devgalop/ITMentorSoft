from pydantic import BaseModel


class GetAvailableRolesResponse(BaseModel):
    is_success: bool
    roles: list[str]
