from typing import Type
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.assessments.shared.assessment import Assessment, AssessmentQuiz
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.qualifier_service import QualifierResult
from src.infrastructure.database.sqllite.models.sqllite_assessment_mapper import (
    SqlliteAssessmentMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_assessment_model import (
    AssessmentEntity,
)


class SqlliteAssessmentRepository(AssessmentRepository):
    def __init__(
        self, session_factory: AsyncSession, mapper: Type[SqlliteAssessmentMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def save_assessment(self, assessment: AssessmentQuiz):
        assessment_entity = self.mapper.quiz_to_assessment_entity(assessment)
        self.session_factory.add(assessment_entity)
        for question in assessment.questions:
            entity = self.mapper.quiz_question_entity(assessment, question)
            self.session_factory.add(entity)
        await self.session_factory.commit()

    async def save_assessment_answers(self, assessment: Assessment):
        for answer in assessment.answers:
            self.session_factory.add(self.mapper.answer_to_entity(answer))
        await self.session_factory.commit()

    async def get_assessment(self, assessment_id: str) -> Assessment | None:
        smt = (
            select(AssessmentEntity)
            .options(selectinload(AssessmentEntity.answers))
            .where(AssessmentEntity.id == assessment_id)
        )
        result = await self.session_factory.execute(smt)
        assessment_entity = result.scalars().first()
        if not assessment_entity:
            return None
        return self.mapper.to_model(assessment_entity)

    async def has_first_assessment(self, user_id: str) -> bool:
        smt = (
            select(AssessmentEntity).where(AssessmentEntity.user_id == user_id).limit(1)
        )
        result = await self.session_factory.execute(smt)
        assessment_entity = result.scalars().first()
        return assessment_entity is not None

    async def get_questions_per_quiz(self, assessment_id: str) -> list[str]:
        smt = (
            select(AssessmentEntity)
            .options(selectinload(AssessmentEntity.questions))
            .where(AssessmentEntity.id == assessment_id)
        )
        result = await self.session_factory.execute(smt)
        assessment_entity = result.scalars().first()
        if not assessment_entity:
            return []
        return self.mapper.quiz_to_model(assessment_entity).questions

    async def get_assessment_quiz(self, assessment_id: str) -> AssessmentQuiz | None:
        smt = (
            select(AssessmentEntity)
            .options(selectinload(AssessmentEntity.questions))
            .where(AssessmentEntity.id == assessment_id)
        )
        result = await self.session_factory.execute(smt)
        assessment_entity = result.scalars().first()
        if not assessment_entity:
            return None
        return self.mapper.quiz_to_model(assessment_entity)

    async def save_assessment_qualification(self, qualifier_result: QualifierResult):
        qualification_entity = self.mapper.qualifier_result_to_entity(qualifier_result)
        self.session_factory.add(qualification_entity)
        for key_concept in qualifier_result.key_concepts_detected:
            key_concept_entity = self.mapper.qualifier_result_key_concept_to_entity(
                qualification_entity.id, key_concept
            )
            self.session_factory.add(key_concept_entity)
        for misconception in qualifier_result.misconceptions_detected:
            misconception_entity = self.mapper.qualifier_result_misconception_to_entity(
                qualification_entity.id, misconception
            )
            self.session_factory.add(misconception_entity)
        await self.session_factory.commit()
