from src.features.reports.get_all_students.get_all_students_request import (
    GetAllStudentsRequest,
)
from src.features.reports.get_all_students.get_all_students_response import (
    GetAllStudentsResponse,
    PaginatedStudentResult,
    StudentClassification,
)
from src.features.reports.shared.student_report_service import (
    GetStudentsResponse,
    StudentReportService,
)


class GetAllStudentsHandler:
    def __init__(self, report_service: StudentReportService):
        self.report_service = report_service

    async def handle(self, request: GetAllStudentsRequest) -> GetAllStudentsResponse:
        """Handle the request to get all students.

        Args:
            request (GetAllStudentsRequest): The request containing pagination parameters.

        Returns:
            GetAllStudentsResponse: The response containing the list of students.
        """
        response = await self.report_service.get_all_students(
            request.page, request.page_size
        )
        if not response.students or not response.is_success:
            return GetAllStudentsResponse(
                is_success=response.is_success,
                message=response.message,
                result=None,
            )
        return GetAllStudentsResponse(
            is_success=response.is_success,
            message=response.message,
            result=self.map_to_response(response),
        )

    def map_to_response(self, response: GetStudentsResponse) -> PaginatedStudentResult:
        """Map the GetStudentsResponse object to PaginatedStudentResult.

        Args:
            response (GetStudentsResponse): The GetStudentsResponse object.

        Returns:
            PaginatedStudentResult: The mapped PaginatedStudentResult object.
        """
        if not response or not response.students:
            return PaginatedStudentResult(students=[], total_students=0, page=0)
        return PaginatedStudentResult(
            students=[
                StudentClassification(
                    student_id=student.student_id,
                    student_name=student.student_name,
                    knowledge_classification=student.knowledge_classification,
                )
                for student in response.students.students
            ],
            total_students=response.students.total_students,
            page=response.students.page,
        )
