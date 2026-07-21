from src.features.reports.shared.student_report import (
    StudentBasicSummary,
    StudentKnowledgeProfile,
)
from src.infrastructure.database.sqllite.models.sqllite_assessment_model import (
    ClassificationResultEntity,
    TopicResultEntity,
)


class SqlliteReportMapper:
    @staticmethod
    def from_classification_result_to_student_basic_summary(
        request: ClassificationResultEntity,
    ) -> StudentBasicSummary:
        student_name = request.user.username if request.user else "Unknown"

        return StudentBasicSummary(
            student_id=request.user_id,
            student_name=student_name,
            knowledge_classification=request.classification,
        )

    @staticmethod
    def to_knowledge_profile(entity: TopicResultEntity) -> StudentKnowledgeProfile:
        return StudentKnowledgeProfile(
            topic=entity.topic,
            score=entity.score,
        )
