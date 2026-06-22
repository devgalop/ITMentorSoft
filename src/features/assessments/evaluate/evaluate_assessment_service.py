from src.features.assessments.shared.assessment import Assessment
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.qualifier_service import (
    QualifierPrompt,
    QualifierResult,
    QualifierService,
)
from src.features.assessments.shared.questions_repository import QuestionRepository

EVALUATION_MODE = "normal"


class EvaluateAssessmentService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        qualifier_service: QualifierService,
        question_repository: QuestionRepository,
    ):
        self.assessment_repository = assessment_repository
        self.qualifier_service = qualifier_service
        self.question_repository = question_repository

    async def evaluate_answers(self, assessment: Assessment):
        evaluation_results: list[QualifierResult] = []
        for answer in assessment.answers:
            rubric = await self.question_repository.get_question_rubric(
                answer.question_id
            )
            if not rubric:
                continue
            evaluation_results.append(
                await self.qualifier_service.qualify(
                    QualifierPrompt(
                        rubric=rubric,
                        qualifier_mode=EVALUATION_MODE,
                        user_id=assessment.user_id,
                        user_answer=answer.answer,
                        assessment_id=assessment.assessment_id,
                        answer_id=answer.answer_id,
                    )
                )
            )

        for result in evaluation_results:
            await self.assessment_repository.save_assessment_qualification(result)
