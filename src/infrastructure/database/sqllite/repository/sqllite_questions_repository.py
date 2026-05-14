from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.assessments.shared.question import EvaluativeQuestion, Question
from src.features.assessments.shared.questions_repository import QuestionRepository
from src.infrastructure.database.sqllite.models.sqllite_question_mapper import (
    SqlliteQuestionMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_question_model import (
    QuestionEntity,
)


class SqlliteQuestionsRepository(QuestionRepository):
    def __init__(
        self, session_factory: AsyncSession, mapper: Type[SqlliteQuestionMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def save_question(self, question: Question):
        entity = self.mapper.to_entity(question)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_question(self, question_id: str) -> EvaluativeQuestion | None:
        smt = select(QuestionEntity).where(QuestionEntity.id == question_id)
        result = await self.session_factory.execute(smt)
        question_entity = result.scalars().first()
        if not question_entity:
            return None
        return self.mapper.to_evaluative_model(question_entity)

    async def get_all_questions(self) -> list[EvaluativeQuestion]:
        smt = select(QuestionEntity)
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return [self.mapper.to_evaluative_model(entity) for entity in question_entities]

    async def get_question_rubric(self, question_id: str) -> Question | None:
        smt = select(QuestionEntity).where(QuestionEntity.id == question_id)
        result = await self.session_factory.execute(smt)
        question_entity = result.scalars().first()
        if not question_entity:
            return None
        return self.mapper.to_model(question_entity)
