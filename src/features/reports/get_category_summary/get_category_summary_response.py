from pydantic import BaseModel


class CategorySummary(BaseModel):
    category: str
    total_students: int


class GetCategorySummaryResponse(BaseModel):
    is_success: bool
    message: str
    category_summary: CategorySummary
