from fastapi.params import Depends
from typing import Annotated

from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.dependencies import get_assessment_repository
from src.features.reports.get_student_progress.get_student_progress_handler import (
    GetStudentProgressHandler,
)
from src.features.reports.get_student_summary.get_student_summary_handler import (
    GetStudentSummaryHandler,
)
from src.features.reports.shared.student_report_service import StudentReportService
from src.features.user_management.shared.dependencies import get_user_repository
from src.features.user_management.shared.user_repository import UserRepository


def get_student_report_service(
    assessment_repository: Annotated[
        AssessmentRepository, Depends(get_assessment_repository)
    ],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> StudentReportService:
    return StudentReportService(
        assessment_repository=assessment_repository, user_repository=user_repository
    )


def get_get_student_summary_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetStudentSummaryHandler:
    return GetStudentSummaryHandler(student_report_service=student_report_service)


def get_get_student_progress_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetStudentProgressHandler:
    return GetStudentProgressHandler(student_report_service=student_report_service)
