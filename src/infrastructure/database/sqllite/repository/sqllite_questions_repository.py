from typing import Type
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    PaginatedQuestionsResult,
    Question,
    QuestionStatus,
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

    async def get_question_rubrics_bulk(
        self, question_ids: list[str]
    ) -> dict[str, Question]:
        if not question_ids:
            return {}
        smt = (
            select(QuestionEntity)
            .options(selectinload(QuestionEntity.rubric))
            .where(QuestionEntity.id.in_(question_ids))
        )
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return {entity.id: self.mapper.to_model(entity) for entity in question_entities}

    async def update_question(self, question: Question):
        smt = (
            select(QuestionEntity)
            .options(selectinload(QuestionEntity.rubric))
            .where(QuestionEntity.id == question.question_id)
        )
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

    async def get_question_categories(self, version: int) -> list[str]:
        smt = (
            select(QuestionEntity.classification)
            .where(
                QuestionEntity.version == version,
                QuestionEntity.status == QuestionStatus.PUBLISHED.value,
            )
            .distinct()
        )
        result = await self.session_factory.execute(smt)
        categories = result.scalars().all()
        if not categories:
            return []
        return list(categories)

    async def get_all_questions_paginated(
        self, page: int, page_size: int
    ) -> PaginatedQuestionsResult:
        """Get all questions with pagination

        Args:
            page (int): The zero-based page index.
            page_size (int): The number of items per page.

        Returns:
            PaginatedQuestionsResult: The paginated result containing the items for the requested page and the total count of all records. If there are no questions, returns an empty list and a total count of 0.
        """
        count_smt = select(func.count()).select_from(QuestionEntity)
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedQuestionsResult(items=[], total=0)

        smt = (
            select(QuestionEntity)
            .options(selectinload(QuestionEntity.rubric))
            .offset(page * page_size)
            .limit(page_size)
        )
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        questions = [
            self.mapper.to_detailed_model(entity) for entity in question_entities
        ]

        return PaginatedQuestionsResult(items=questions, total=total)
