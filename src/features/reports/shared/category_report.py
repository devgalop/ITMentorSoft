from pydantic import BaseModel


class CategorySummary(BaseModel):
    category: str
    total_students: int
