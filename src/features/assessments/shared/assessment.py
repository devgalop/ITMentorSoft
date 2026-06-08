from datetime import datetime
import uuid


class AssessmentAnswer:
    """Represents an answer to a question in an assessment"""

    def __init__(self, question_id: str, answer: str, time_taken_seconds: int):
        self.question_id = question_id
        self.answer = answer
        self.time_taken_seconds = time_taken_seconds


class Assessment:
    """Represents an assessment taken by a user"""

    def __init__(
        self,
        assessment_id: str,
        user_id: str,
        created_at: datetime,
        answers: list[AssessmentAnswer],
    ):
        self.assessment_id = assessment_id
        self.user_id = user_id
        self.created_at = created_at
        self.answers = answers


class AssessmentQuiz:
    def __init__(self, user_id: str, created_at: datetime, questions: list[str]):
        self.assessment_id = uuid.uuid4().hex
        self.user_id = user_id
        self.created_at = created_at
        self.questions = questions
