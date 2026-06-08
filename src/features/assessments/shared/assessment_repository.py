from abc import ABC, abstractmethod

from src.features.assessments.shared.assessment import Assessment, AssessmentQuiz


class AssessmentRepository(ABC):

    @abstractmethod
    async def save_assessment(self, assessment: AssessmentQuiz):
        """Save an assessment

        Args:
            assessment: The assessment to be saved.
        """
        pass

    @abstractmethod
    async def save_assessment_answers(self, assessment: Assessment):
        """Save the answers of an assessment

        Args:
            assessment: The assessment with the answers to be saved.
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

    @abstractmethod
    async def get_questions_per_quiz(self, assessment_id: str) -> list[str]:
        """Obtain the questions of an assessment quiz by Id

        Args:
            assessment_id (str): The ID of the assessment quiz to retrieve the questions from.

        Returns:
            A list of question IDs corresponding to the given assessment quiz ID.
        """
        pass
