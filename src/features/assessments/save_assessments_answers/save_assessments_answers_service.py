from datetime import datetime

from src.features.assessments.save_assessments_answers.save_assessments_answers_request import (
    SaveAssessmentsAnswersRequest,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_response import (
    SaveAssessmentsAnswersResponse,
)
from src.features.assessments.shared.assessment import Assessment, AssessmentAnswer
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.user_management.shared.user_repository import UserRepository


class SaveAssessmentsAnswersService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        user_repository: UserRepository,
    ):
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository

    async def save_assessment_answers(
        self, request: SaveAssessmentsAnswersRequest
    ) -> SaveAssessmentsAnswersResponse:
        """Validate and save the answers of an assessment

        Args:
            request (SaveAssessmentsAnswersRequest): Assessment answers to be saved

        Returns:
            SaveAssessmentsAnswersResponse: The result of the operation
        """
        try:
            user = await self.user_repository.get_user_by_id(request.user_id)
            if not user:
                return SaveAssessmentsAnswersResponse(
                    is_success=False, message="User not found."
                )
            questions = await self.assessment_repository.get_questions_per_quiz(
                request.assessment_id
            )
            if not questions or len(questions) != len(request.answers):
                return SaveAssessmentsAnswersResponse(
                    is_success=False, message="Invalid assessment ID or answers."
                )
            answers: list[AssessmentAnswer] = []
            for answer in request.answers:
                if answer.question_id not in questions:
                    return SaveAssessmentsAnswersResponse(
                        is_success=False,
                        message=f"Invalid question ID: {answer.question_id}.",
                    )
                answers.append(
                    AssessmentAnswer(
                        question_id=answer.question_id,
                        answer=answer.answer,
                        time_taken_seconds=answer.takes_time_seconds,
                    )
                )

            assessment = Assessment(
                user_id=request.user_id,
                created_at=datetime.now(),
                answers=answers,
            )

            assessment.set_id(request.assessment_id)

            await self.assessment_repository.save_assessment_answers(assessment)

            return SaveAssessmentsAnswersResponse(
                is_success=True, message="Assessment answers saved successfully."
            )
        except Exception as e:
            return SaveAssessmentsAnswersResponse(
                is_success=False, message=f"An error occurred: {str(e)}"
            )
