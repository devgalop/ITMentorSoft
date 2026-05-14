from abc import ABC, abstractmethod

from src.features.assessments.shared.question import EvaluativeQuestion, Question


class QuestionRepository(ABC):

    @abstractmethod
    async def get_question(self, question_id: str) -> EvaluativeQuestion | None:
        """Obtain a question by Id

        Args:
            question_id (str): The ID of the question to retrieve.

        Returns:
            EvaluativeQuestion | None: The question corresponding to the given ID, or None if not found.
        """
        pass

    @abstractmethod
    async def get_all_questions(self) -> list[EvaluativeQuestion]:
        """Obtain all questions

        Returns:
            list[EvaluativeQuestion]: A list of all questions.
        """
        pass

    @abstractmethod
    async def get_question_rubric(self, question_id: str) -> Question | None:
        """Obtain the rubric for a question by ID

        Args:
            question_id (str): The ID of the question to retrieve the rubric for.

        Returns:
            Question | None: The question with its rubric corresponding to the given ID, or None if not found.
        """
        pass

    @abstractmethod
    async def save_question(self, question: Question):
        """Save a question

        Args:
            question (Question): The question to be saved.
        """
        pass

    @abstractmethod
    async def update_question(self, question: Question):
        """Update a question

        Args:
            question (Question): The question to be updated.
        """
        pass
