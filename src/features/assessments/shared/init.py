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
from src.features.assessments.save_assessments_answers.save_assessments_answers_endpoint import (
    router as save_assessment_answers_router,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_endpoint import (
    router as get_assessment_by_topic_router,
)
from src.features.assessments.get_question_categories.get_question_categories_endpoint import (
    router as get_question_categories_router,
)

router = APIRouter()
router.include_router(register_question_router)
router.include_router(get_question_by_id_router)
router.include_router(get_questions_by_level_router)
router.include_router(get_questions_by_category_router)
router.include_router(update_question_router)
router.include_router(get_assessment_router)
router.include_router(save_assessment_answers_router)
router.include_router(get_assessment_by_topic_router)
router.include_router(get_question_categories_router)
