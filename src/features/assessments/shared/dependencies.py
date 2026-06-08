from fastapi.params import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.assessments.get_assessment.get_assessment_handler import (
    GetAssessmentHandler,
)
from src.features.assessments.get_assessment.get_assessment_service import (
    GetAssessmentService,
)
from src.features.assessments.get_question_by_id.get_question_by_id_handler import (
    GetQuestionByIdHandler,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_handler import (
    GetQuestionsByLevelHandler,
)
from src.features.assessments.get_questions_by_category.get_questions_by_category_handler import (
    GetQuestionsByCategoryHandler,
)
from src.features.assessments.register_question.register_question_handler import (
    RegisterQuestionHandler,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_handler import (
    SaveAssessmentsAnswersHandler,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_service import (
    SaveAssessmentsAnswersService,
)
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.question_assessment_repository import (
    QuestionAssessmentRepository,
)
from src.features.assessments.shared.questions_cache_repository import (
    QuestionsCacheRepository,
)
from src.features.assessments.update_question.update_question_handler import (
    UpdateQuestionHandler,
)
from src.features.assessments.shared.question import QuestionBuilder
from src.features.assessments.shared.questions_repository import QuestionRepository
from src.features.user_management.shared.dependencies import get_user_repository
from src.features.user_management.shared.user_repository import UserRepository
from src.infrastructure.database.sqllite.models.sqllite_assessment_mapper import (
    SqlliteAssessmentMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_question_mapper import (
    SqlliteQuestionMapper,
)
from src.infrastructure.database.sqllite.repository.sqllite_assessment_repository import (
    SqlliteAssessmentRepository,
)
from src.infrastructure.database.sqllite.repository.sqllite_questions_assessment_repository import (
    SqlLiteQuestionsAssessmentRepository,
)
from src.infrastructure.database.sqllite.repository.sqllite_questions_repository import (
    SqlliteQuestionsRepository,
)
from src.infrastructure.database.sqllite.shared.sqllite_database_session import get_db


def get_question_repository(
    session_factory: Annotated[AsyncSession, Depends(get_db)],
) -> QuestionRepository:
    return SqlliteQuestionsRepository(session_factory, SqlliteQuestionMapper)


def get_question_assessment_repository(
    session_factory: Annotated[AsyncSession, Depends(get_db)],
) -> QuestionAssessmentRepository:
    return SqlLiteQuestionsAssessmentRepository(session_factory, SqlliteQuestionMapper)


def get_assessment_repository(
    session_factory: Annotated[AsyncSession, Depends(get_db)],
) -> AssessmentRepository:
    return SqlliteAssessmentRepository(session_factory, SqlliteAssessmentMapper)


def get_questions_cache_repository(
    question_assessment_repository: Annotated[
        QuestionAssessmentRepository, Depends(get_question_assessment_repository)
    ],
) -> QuestionAssessmentRepository:
    return QuestionsCacheRepository(
        assessment_repository=question_assessment_repository
    )


def get_register_question_handler(
    question_repository: Annotated[
        QuestionRepository, Depends(get_question_repository)
    ],
) -> RegisterQuestionHandler:
    return RegisterQuestionHandler(
        question_repository=question_repository,
        question_builder=QuestionBuilder,
    )


def get_get_question_by_id_handler(
    question_repository: Annotated[
        QuestionRepository, Depends(get_question_repository)
    ],
) -> GetQuestionByIdHandler:
    return GetQuestionByIdHandler(question_repository=question_repository)


def get_update_question_handler(
    question_repository: Annotated[
        QuestionRepository, Depends(get_question_repository)
    ],
) -> UpdateQuestionHandler:
    return UpdateQuestionHandler(question_repository=question_repository)


def get_get_questions_by_level_handler(
    question_repository: Annotated[
        QuestionAssessmentRepository, Depends(get_questions_cache_repository)
    ],
) -> GetQuestionsByLevelHandler:
    return GetQuestionsByLevelHandler(question_repository=question_repository)


def get_get_questions_by_category_handler(
    question_repository: Annotated[
        QuestionAssessmentRepository, Depends(get_questions_cache_repository)
    ],
) -> GetQuestionsByCategoryHandler:
    return GetQuestionsByCategoryHandler(question_repository=question_repository)


def get_assessment_service(
    question_repository: Annotated[
        QuestionAssessmentRepository, Depends(get_questions_cache_repository)
    ],
    assessment_repository: Annotated[
        AssessmentRepository, Depends(get_assessment_repository)
    ],
) -> GetAssessmentService:
    return GetAssessmentService(
        question_repository=question_repository,
        assessment_repository=assessment_repository,
    )


def get_get_assessment_handler(
    get_assessment_service: Annotated[
        GetAssessmentService, Depends(get_assessment_service)
    ],
) -> GetAssessmentHandler:
    return GetAssessmentHandler(get_assessment_service=get_assessment_service)


def get_save_assessment_answers_service(
    assessment_repository: Annotated[
        AssessmentRepository, Depends(get_assessment_repository)
    ],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> SaveAssessmentsAnswersService:
    return SaveAssessmentsAnswersService(
        assessment_repository=assessment_repository,
        user_repository=user_repository,
    )


def get_save_assessment_answers_handler(
    service: Annotated[
        SaveAssessmentsAnswersService, Depends(get_save_assessment_answers_service)
    ],
) -> SaveAssessmentsAnswersHandler:
    return SaveAssessmentsAnswersHandler(assessment_service=service)
