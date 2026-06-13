from abc import ABC, abstractmethod

from src.features.assessments.shared.question import Question


class QualifierPrompt:
    def __init__(
        self, rubric: Question, qualifier_mode: str, user_id: str, user_answer: str
    ):
        self.rubric = rubric
        self.qualifier_mode = qualifier_mode
        self.user_id = user_id
        self.user_answer = user_answer


class QualifierResult:
    def __init__(
        self,
        question_id: str,
        user_id: str,
        score: int,
        feedback: str,
        key_concepts_detected: list[str],
        misconceptions_detected: list[str],
    ):
        self.question_id = question_id
        self.user_id = user_id
        self.score = score
        self.feedback = feedback
        self.key_concepts_detected = key_concepts_detected or []
        self.misconceptions_detected = misconceptions_detected or []


class QualifierService(ABC):

    @abstractmethod
    async def qualify(self, qualifier_prompt: QualifierPrompt) -> QualifierResult:
        """Assign a score based on the user's answer to a question, and provide feedback.

        Args:
            qualifier_prompt (QualifierPrompt): The prompt containing the question, user answer, and qualifier mode.

        Returns:
            QualifierResult: The result of the qualification, including score, feedback, key concepts detected, and misconceptions detected.
        """
        pass
