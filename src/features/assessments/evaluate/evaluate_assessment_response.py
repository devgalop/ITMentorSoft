from src.features.assessments.shared.classification_service import (
    QuestionAnswerQualification,
)


class EvaluateAssessmentResponse:
    def __init__(
        self,
        is_success: bool,
        message: str,
        qualifications: list[QuestionAnswerQualification] | None = None,
    ):
        self.is_success = is_success
        self.message = message
        self.qualifications = qualifications
