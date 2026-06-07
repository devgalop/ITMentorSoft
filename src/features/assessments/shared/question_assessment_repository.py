from abc import ABC, abstractmethod

from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    QuestionDifficulty,
)


class QuestionAssessmentRepository(ABC):

    @abstractmethod
    async def get_question_by_level(
        self, difficulty: QuestionDifficulty
    ) -> list[EvaluativeQuestion]:
        """Obtain questions by difficulty level

        Args:
            difficulty (QuestionDifficulty): The difficulty level to filter questions by.

        Returns:
            list[EvaluativeQuestion]: A list of questions matching the specified difficulty level.
        """
        pass

    @abstractmethod
    async def get_questions_by_category(
        self, category: str
    ) -> list[EvaluativeQuestion]:
        """Obtain questions by category

        Args:
            category (str): The category to filter questions by.

        Returns:
            list[EvaluativeQuestion]: A list of questions matching the specified category.
        """
        pass
