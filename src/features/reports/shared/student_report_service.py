from pydantic import BaseModel
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.reports.shared.student_report import StudentProgress, StudentSummary
from src.features.user_management.shared.user_repository import UserRepository


class GetSummaryResponse(BaseModel):
    is_success: bool
    message: str
    student_summary: StudentSummary | None = None


class GetProgressByTopic(BaseModel):
    is_success: bool
    message: str
    historical_progress: StudentProgress | None = None


class StudentReportService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        user_repository: UserRepository,
    ):
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository

    async def get_student_summary(self, user_id: str) -> GetSummaryResponse:
        """Obtain the student summary by user ID

        Args:
            user_id (str): The ID of the user to retrieve the student summary for.

        Returns:
            GetSummaryResponse: The student summary corresponding to the given user ID.
        """
        student_found = await self.user_repository.get_user_by_id(user_id)
        if not student_found:
            return GetSummaryResponse(
                is_success=False, message="Student not found", student_summary=None
            )

        response = await self.assessment_repository.get_student_summary(user_id)
        if not response or not response.knowledge_profiles:
            return GetSummaryResponse(
                is_success=False,
                message="Student summary not found",
                student_summary=None,
            )

        return GetSummaryResponse(
            is_success=True,
            message="Student summary retrieved successfully",
            student_summary=response,
        )

    async def get_student_progress(self, user_id: str) -> GetProgressByTopic:
        """Obtain the student progress by user ID

        Args:
            user_id (str): The ID of the user to retrieve the student progress for.

        Returns:
            GetProgressByTopic: The student progress corresponding to the given user ID.
        """
        student_found = await self.user_repository.get_user_by_id(user_id)
        if not student_found:
            return GetProgressByTopic(
                is_success=False, message="Student not found", historical_progress=None
            )

        response = await self.assessment_repository.get_student_progress(user_id)
        if not response or not response.historical_progress:
            return GetProgressByTopic(
                is_success=False,
                message="Student progress not found",
                historical_progress=None,
            )

        return GetProgressByTopic(
            is_success=True,
            message="Student progress retrieved successfully",
            historical_progress=response,
        )
