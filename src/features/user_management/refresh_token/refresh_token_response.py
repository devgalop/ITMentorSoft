from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    is_successful: bool
    access_token: str | None
    refresh_token: str | None
    expiration_time: float | None
