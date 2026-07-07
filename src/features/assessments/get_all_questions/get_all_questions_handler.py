from src.features.assessments.get_all_questions.get_all_questions_request import (
    GetAllQuestionsRequest,
)
from src.features.assessments.get_all_questions.get_all_questions_response import (
    GetAllQuestionsResponse,
)
from src.features.assessments.shared.questions_repository import QuestionRepository


class GetAllQuestionsHandler:
    def __init__(self, questions_repository: QuestionRepository):
        self.questions_repository = questions_repository

    async def handle(self, request: GetAllQuestionsRequest) -> GetAllQuestionsResponse:
        paginated_result = await self.questions_repository.get_all_questions_paginated(
            request.page, request.page_size
        )
        if not paginated_result.items:
            return GetAllQuestionsResponse(
                is_success=False, message="No questions found.", items=[], total=0
            )
        return GetAllQuestionsResponse(
            is_success=True,
            message="Successfully retrieved all questions.",
            items=paginated_result.items,
            total=paginated_result.total,
        )
