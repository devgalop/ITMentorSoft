from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    QuestionDifficulty,
)
from src.features.assessments.shared.question_assessment_repository import (
    QuestionAssessmentRepository,
)
from src.infrastructure.database.sqllite.models.sqllite_question_mapper import (
    SqlliteQuestionMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_question_model import (
    QuestionEntity,
)


class SqlLiteQuestionsAssessmentRepository(QuestionAssessmentRepository):
    def __init__(
        self, session_factory: AsyncSession, mapper: Type[SqlliteQuestionMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def get_question_by_level(
        self, difficulty: QuestionDifficulty
    ) -> list[EvaluativeQuestion]:
        smt = select(QuestionEntity).where(
            QuestionEntity.difficulty == difficulty.value
        )
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return [self.mapper.to_evaluative_model(entity) for entity in question_entities]

    async def get_questions_by_category(
        self, category: str
    ) -> list[EvaluativeQuestion]:
        smt = select(QuestionEntity).where(QuestionEntity.classification == category)
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return [self.mapper.to_evaluative_model(entity) for entity in question_entities]
