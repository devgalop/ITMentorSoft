from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.assessments.shared.assessment import Assessment, AssessmentQuiz
from src.features.assessments.shared.assessment_repository import AssessmentRepository
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
        entity = self.mapper.quiz_to_entity(assessment)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def save_assessment_answers(self, assessment: Assessment):
        entity = self.mapper.to_entity(assessment)
        self.session_factory.add(entity)
        for answer in entity.answers:
            self.session_factory.add(answer)
        await self.session_factory.commit()

    async def get_assessment(self, assessment_id: str) -> Assessment | None:
        smt = select(AssessmentEntity).where(AssessmentEntity.id == assessment_id)
        result = await self.session_factory.execute(smt)
        assessment_entity = result.scalars().first()
        if not assessment_entity:
            return None
        return self.mapper.to_model(assessment_entity)

    async def has_first_assessment(self, user_id: str) -> bool:
        smt = select(AssessmentEntity).where(AssessmentEntity.user_id == user_id)
        result = await self.session_factory.execute(smt)
        assessment_entity = result.scalars().first()
        return assessment_entity is not None
