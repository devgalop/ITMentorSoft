from src.features.assessments.evaluate.evaluate_assessment_contract import (
    EvaluateAssessmentContract,
)
from src.features.assessments.evaluate.evaluate_assessment_request import (
    EvaluateAssessmentRequest,
)
from src.features.assessments.evaluate.evaluate_assessment_response import (
    EvaluateAssessmentResponse,
)
from src.features.assessments.evaluate.evaluate_assessment_service import (
    EvaluateAssessmentService,
)


class EvaluateAssessmentHandler(EvaluateAssessmentContract):
    def __init__(self, evaluate_assessment_service: EvaluateAssessmentService):
        self.evaluate_assessment_service = evaluate_assessment_service

    async def evaluate(
        self, request: EvaluateAssessmentRequest
    ) -> EvaluateAssessmentResponse:
        if not request.assessment:
            raise ValueError("Assessment data is required for evaluation.")
        result = await self.evaluate_assessment_service.evaluate_answers(
            request.assessment
        )
        if not result:
            return EvaluateAssessmentResponse(
                is_success=False,
                message="No qualifications generated for the assessment.",
                qualifications=None,
            )
        return EvaluateAssessmentResponse(
            is_success=True,
            message="Assessment evaluation completed successfully.",
            qualifications=result,
        )
