import uuid

from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
from src.features.assessments.get_assessment.get_assessment_response import (
    GetAssessmentResponse,
)
from src.features.assessments.get_assessment.get_assessment_service import (
    GetAssessmentService,
)


class GetAssessmentHandler:
    def __init__(self, get_assessment_service: GetAssessmentService):
        self.get_assessment_service = get_assessment_service

    async def handle(self, request: GetAssessmentRequest) -> GetAssessmentResponse:
        try:
            questions = await self.get_assessment_service.generate_assessment(request)
            return GetAssessmentResponse(
                is_success=True,
                message="Assessment retrieved successfully",
                assessment_id=uuid.uuid4().hex,
                questions=questions,
            )
        except Exception as e:
            return GetAssessmentResponse(
                is_success=False,
                message=f"Failed to retrieve assessment: {str(e)}",
                assessment_id=None,
                questions=None,
            )
