from typing import Type
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    Question,
)
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
        rubric_entities = self.mapper.to_rubric_score_entities(
            question.question_id, question.rubric
        )
        self.session_factory.add(entity)
        for rubric_entity in rubric_entities:
            self.session_factory.add(rubric_entity)
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
        smt = (
            select(QuestionEntity)
            .options(selectinload(QuestionEntity.rubric))
            .where(QuestionEntity.id == question_id)
        )
        result = await self.session_factory.execute(smt)
        question_entity = result.scalars().first()
        if not question_entity:
            return None
        return self.mapper.to_model(question_entity)

    async def update_question(self, question: Question):
        smt = select(QuestionEntity).where(QuestionEntity.id == question.question_id)
        result = await self.session_factory.execute(smt)
        entity = result.scalars().first()
        if not entity:
            return
        entity.text = question.text_to_evaluate
        entity.concept = question.concept
        entity.definition = question.definition
        entity.simple_explanation = question.simple_explanation
        entity.correct_sample = question.correct_sample
        entity.wrong_sample = question.wrong_sample
        entity.common_misconceptions = "|".join(question.common_misconception)
        entity.semantic_keywords = "|".join(question.semantic_keywords)
        entity.status = question.status.value
        # Replace rubric: delete old, insert new
        for rubric in entity.rubric:
            await self.session_factory.delete(rubric)
        new_rubric_entities = self.mapper.to_rubric_score_entities(
            question.question_id, question.rubric
        )
        for rubric_entity in new_rubric_entities:
            self.session_factory.add(rubric_entity)
        await self.session_factory.commit()
