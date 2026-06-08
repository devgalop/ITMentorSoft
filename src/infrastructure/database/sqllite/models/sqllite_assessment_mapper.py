from src.features.assessments.shared.assessment import (
    Assessment,
    AssessmentAnswer,
    AssessmentQuiz,
)
from src.infrastructure.database.sqllite.models.sqllite_assessment_model import (
    AssessmentAnswerEntity,
    AssessmentEntity,
    AssessmentQuizEntity,
)


class SqlliteAssessmentMapper:
    @staticmethod
    def to_entity(request: Assessment) -> AssessmentEntity:
        answers = [
            SqlliteAssessmentAnswerMapper.to_entity(ans) for ans in request.answers
        ]
        return AssessmentEntity(
            id=request.assessment_id,
            user_id=request.user_id,
            created_at=request.created_at,
            answers=answers,
        )

    @staticmethod
    def to_model(entity: AssessmentEntity) -> Assessment:
        answers = [
            SqlliteAssessmentAnswerMapper.to_model(ans) for ans in entity.answers
        ]
        assessment = Assessment(
            user_id=entity.user_id, created_at=entity.created_at, answers=answers
        )
        assessment.set_id(entity.id)
        return assessment

    @staticmethod
    def quiz_to_entity(request: AssessmentQuiz) -> AssessmentQuizEntity:
        return AssessmentQuizEntity(
            id=request.assessment_id,
            user_id=request.user_id,
            created_at=request.created_at,
            questions=",".join(request.questions),
        )

    @staticmethod
    def quiz_to_model(entity: AssessmentQuizEntity) -> AssessmentQuiz:
        questions = entity.questions.split(",") if entity.questions else []
        assessment_quiz = AssessmentQuiz(
            user_id=entity.user_id, created_at=entity.created_at, questions=questions
        )
        assessment_quiz.assessment_id = entity.id
        return assessment_quiz


class SqlliteAssessmentAnswerMapper:
    @staticmethod
    def to_entity(request: AssessmentAnswer) -> AssessmentAnswerEntity:
        return AssessmentAnswerEntity(
            question_id=request.question_id,
            answer=request.answer,
            time_taken_seconds=request.time_taken_seconds,
        )

    @staticmethod
    def to_model(entity: AssessmentAnswerEntity) -> AssessmentAnswer:
        return AssessmentAnswer(
            question_id=entity.question_id,
            answer=entity.answer,
            time_taken_seconds=entity.time_taken_seconds,
        )
