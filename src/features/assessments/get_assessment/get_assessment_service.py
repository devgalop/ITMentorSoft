from secrets import SystemRandom


from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
from src.features.assessments.get_assessment.get_assessment_response import (
    EvaluativeQuestionData,
)
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    QuestionDifficulty,
)
from src.features.assessments.shared.question_assessment_repository import (
    QuestionAssessmentRepository,
)

_rng = SystemRandom()


class GetRandomQuestionsRequest:
    def __init__(
        self,
        number_of_questions: int,
        difficulty_level: QuestionDifficulty,
    ):
        self.number_of_questions = number_of_questions
        self.difficulty_level = difficulty_level


class GetAssessmentService:
    def __init__(
        self,
        question_repository: QuestionAssessmentRepository,
        assessment_repository: AssessmentRepository,
    ):
        self.question_repository = question_repository
        self.assessment_repository = assessment_repository

    async def generate_assessment(
        self, request: GetAssessmentRequest
    ) -> list[EvaluativeQuestionData]:
        """Generate dynamically assessment questions based on the student's level and the number of questions requested.
        When the assessment is for an initial evaluation, questions are distributed evenly across all difficulty levels.
        For follow-up evaluations, 60% of the questions are selected from the student's current level, while the remaining 40% are distributed among adjacent levels.

        Args:
            request (GetAssessmentRequest): An object containing the student's ID and the number of questions to generate.

        Returns:
            list[EvaluativeQuestionData]: A list of evaluative question data objects representing the generated assessment questions.
        """
        questions: list[EvaluativeQuestionData] = []
        # Se debe implementar la lógica para calcular el numero de preguntas dependiendo del tipo de evaluación (inicial o seguimiento) y el nivel del estudiante
        number_of_questions_base: int = request.number_of_questions // len(
            QuestionDifficulty
        )
        remaining_questions: int = request.number_of_questions % len(QuestionDifficulty)

        for index, difficulty in enumerate(QuestionDifficulty):
            total_questions = number_of_questions_base + (
                1 if index < remaining_questions else 0
            )
            questions += await self.get_random_questions(
                GetRandomQuestionsRequest(
                    number_of_questions=total_questions, difficulty_level=difficulty
                )
            )
        return questions

    async def is_initial_assessment(self, student_id: str) -> bool:
        """Determine if the assessment being generated is the student's initial assessment by checking if the student has taken any previous assessments.

        Args:
            student_id (str): The ID of the student to check.

        Returns:
            bool: True if the assessment is the student's initial assessment, False otherwise.
        """
        return not await self.assessment_repository.has_first_assessment(student_id)

    async def get_random_questions(
        self, request: GetRandomQuestionsRequest
    ) -> list[EvaluativeQuestionData]:
        """Obtain a random selection of questions based on the specified difficulty level and number of questions.

        Args:
            request (GetRandomQuestionsRequest): An object containing the number of questions to retrieve and the desired difficulty level.

        Returns:
            list[EvaluativeQuestionData]: A list of evaluative question data objects representing the randomly selected questions.
        """
        questions = await self.question_repository.get_question_by_level(
            difficulty=request.difficulty_level
        )

        # If the number of questions requested exceeds the available questions, adjust the number to the maximum available.
        if request.number_of_questions > len(questions):
            request.number_of_questions = len(questions)

        questions_selected: list[EvaluativeQuestion] = _rng.sample(
            questions, request.number_of_questions
        )
        return [
            EvaluativeQuestionData(
                question_id=question.question_id,
                text_to_evaluate=question.text_to_evaluate,
            )
            for question in questions_selected
        ]
