from src.features.assessments.save_assessments_answers.save_assessments_answers_request import (
    SaveAssessmentsAnswersRequest,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_response import (
    SaveAssessmentsAnswersResponse,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_service import (
    SaveAssessmentsAnswersService,
)


class SaveAssessmentsAnswersHandler:
    def __init__(self, assessment_service: SaveAssessmentsAnswersService):
        self.assessment_service = assessment_service

    async def handle(
        self, request: SaveAssessmentsAnswersRequest
    ) -> SaveAssessmentsAnswersResponse:
        return await self.assessment_service.save_assessment_answers(request)
