from src.features.assessments.shared.assessment import Assessment
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.qualifier_service import (
    QualifierPrompt,
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
        for answer in assessment.answers:
            rubric = await self.question_repository.get_question_rubric(
                answer.question_id
            )
            if not rubric:
                continue
            evaluation_result = await self.qualifier_service.qualify(
                QualifierPrompt(
                    rubric=rubric,
                    qualifier_mode=EVALUATION_MODE,
                    user_id=assessment.user_id,
                    user_answer=answer.answer,
                )
            )
            print(
                f"Evaluation result for question {answer.question_id}: Score={evaluation_result.score}, Feedback={evaluation_result.feedback}"
            )
