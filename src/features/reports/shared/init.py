from fastapi import APIRouter

from src.features.reports.get_student_summary.get_student_summary_endpoint import (
    router as get_student_summary_router,
)

router = APIRouter()
router.include_router(get_student_summary_router)
