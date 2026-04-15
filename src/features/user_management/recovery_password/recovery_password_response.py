from pydantic import BaseModel

class RecoveryPasswordResponse(BaseModel):
    message: str