from abc import ABC, abstractmethod

from src.features.assessments.shared.assessment import Assessment


class AssessmentRepository(ABC):

    @abstractmethod
    async def save_assessment(self, assessment: Assessment):
        """Save an assessment

        Args:
            assessment: The assessment to be saved.
        """
        pass

    @abstractmethod
    async def get_assessment(self, assessment_id: str) -> Assessment | None:
        """Obtain an assessment by Id

        Args:
            assessment_id (str): The ID of the assessment to retrieve.

        Returns:
            The assessment corresponding to the given ID, or None if not found.
        """
        pass

    @abstractmethod
    async def has_first_assessment(self, user_id: str) -> bool:
        """Check if the user has taken their first assessment

        Args:
            user_id (str): The ID of the user to check.
        Returns:
            True if the user has taken their first assessment, False otherwise.
        """
        pass
