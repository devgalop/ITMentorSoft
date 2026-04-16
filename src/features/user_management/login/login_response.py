from pydantic import BaseModel


class LoginResponse(BaseModel):
    is_successful: bool
    token: str
    expiration_time: float
