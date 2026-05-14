from fastapi import APIRouter

from src.features.assessments.register_question.register_question_endpoint import (
    router as register_question_router,
)

router = APIRouter()
router.include_router(register_question_router)
