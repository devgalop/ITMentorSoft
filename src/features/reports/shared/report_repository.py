from abc import ABC, abstractmethod

from src.features.reports.shared.category_report import CategorySummary
from src.features.reports.shared.student_report import PaginatedStudentSummary


class ReportRepository(ABC):
    @abstractmethod
    async def get_all_students(
        self, page: int, page_size: int
    ) -> PaginatedStudentSummary:
        """Retrieve a list of all students.

        Returns:
            PaginatedStudentSummary: A list of StudentSummary objects representing all students.
        """
        pass

    @abstractmethod
    async def get_all_students_by_category(
        self, category: str, page: int, page_size: int
    ) -> PaginatedStudentSummary:
        """Retrieve a list of all students filtered by a specific category.

        Args:
            category (str): The category to filter students by.

        Returns:
            PaginatedStudentSummary: A list of StudentSummary objects representing students in the specified category.
        """
        pass

    @abstractmethod
    async def get_category_summary(self, category: str) -> CategorySummary:
        """Retrieve a summary of a specific category.

        Args:
            category (str): The category to retrieve the summary for.

        Returns:
            CategorySummary: An object representing the summary of the specified category.
        """
        pass
