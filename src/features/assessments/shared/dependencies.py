from fastapi.params import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.assessments.get_question_by_id.get_question_by_id_handler import (
    GetQuestionByIdHandler,
)
from src.features.assessments.register_question.register_question_handler import (
    RegisterQuestionHandler,
)
from src.features.assessments.update_question.update_question_handler import (
    UpdateQuestionHandler,
)
from src.features.assessments.shared.question import QuestionBuilder
from src.features.assessments.shared.questions_repository import QuestionRepository
from src.infrastructure.database.sqllite.models.sqllite_question_mapper import (
    SqlliteQuestionMapper,
)
from src.infrastructure.database.sqllite.repository.sqllite_questions_repository import (
    SqlliteQuestionsRepository,
)
from src.infrastructure.database.sqllite.shared.sqllite_database_session import get_db


def get_question_repository(
    session_factory: Annotated[AsyncSession, Depends(get_db)],
) -> QuestionRepository:
    return SqlliteQuestionsRepository(session_factory, SqlliteQuestionMapper)


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
