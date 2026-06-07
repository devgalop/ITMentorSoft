from typing import Type

from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from src.features.assessments.register_question.register_question_response import (
    RegisterQuestionResponse,
)
from src.features.assessments.shared.question import (
    Question,
    QuestionBuilder,
    QuestionRubricScore,
)
from src.features.assessments.shared.questions_repository import QuestionRepository


class RegisterQuestionHandler:
    def __init__(
        self,
        question_repository: QuestionRepository,
        question_builder: Type[QuestionBuilder],
    ):
        self.question_repository = question_repository
        self.question_builder = question_builder

    async def handle(
        self, request: RegisterQuestionRequest
    ) -> RegisterQuestionResponse:
        try:
            rubric_scores: list[QuestionRubricScore] = [
                QuestionRubricScore(score=r.score, explanation=r.criteria)
                for r in request.rubric
            ]
            question: Question = (
                self.question_builder()
                .set_text_to_evaluate(request.text)
                .set_concept(request.concept)
                .set_definition(request.definition)
                .set_simple_explanation(request.simple_explanation)
                .set_correct_sample(request.correct_sample)
                .set_wrong_sample(request.wrong_sample)
                .add_common_misconceptions(request.common_misconception)
                .add_semantic_keywords(request.semantic_keywords)
                .add_rubrics(rubric_scores)
                .build()
            )
            await self.question_repository.save_question(question)
            return RegisterQuestionResponse(
                is_success=True,
                message="Question registered successfully",
                question_id=question.question_id,
            )
        except Exception as e:
            return RegisterQuestionResponse(
                is_success=False, message=f"Failed to register question: {str(e)}"
            )
