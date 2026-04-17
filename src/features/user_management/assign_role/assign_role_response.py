from pydantic import BaseModel


class AssignRoleResponse(BaseModel):
    is_success: bool
    message: str
