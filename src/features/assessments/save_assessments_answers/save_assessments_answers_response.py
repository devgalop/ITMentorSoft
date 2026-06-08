from pydantic import BaseModel


class SaveAssessmentsAnswersResponse(BaseModel):
    is_success: bool
    message: str
