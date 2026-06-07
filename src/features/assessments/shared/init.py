from fastapi import APIRouter

from src.features.assessments.get_question_by_id.get_question_by_id_endpoint import (
    router as get_question_by_id_router,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_endpoint import (
    router as get_questions_by_level_router,
)
from src.features.assessments.get_questions_by_category.get_questions_by_category_endpoint import (
    router as get_questions_by_category_router,
)
from src.features.assessments.register_question.register_question_endpoint import (
    router as register_question_router,
)
from src.features.assessments.update_question.update_question_endpoint import (
    router as update_question_router,
)
from src.features.assessments.get_assessment.get_assessment_endpoint import (
    router as get_assessment_router,
)

router = APIRouter()
router.include_router(register_question_router)
router.include_router(get_question_by_id_router)
router.include_router(get_questions_by_level_router)
router.include_router(get_questions_by_category_router)
router.include_router(update_question_router)
router.include_router(get_assessment_router)
