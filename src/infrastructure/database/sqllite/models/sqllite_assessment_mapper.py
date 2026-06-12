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
            assessment_id=entity.id,
            user_id=entity.user_id,
            created_at=entity.created_at,
            answers=answers,
        )
        return assessment

    @staticmethod
    def quiz_question_entity(
        request: AssessmentQuiz, question_id: str
    ) -> AssessmentQuizEntity:
        return AssessmentQuizEntity(
            assessment_id=request.assessment_id,
            question_id=question_id,
            created_at=request.created_at,
        )

    @staticmethod
    def quiz_to_assessment_entity(quiz: AssessmentQuiz) -> AssessmentEntity:
        return AssessmentEntity(
            id=quiz.assessment_id,
            user_id=quiz.user_id,
            created_at=quiz.created_at,
        )

    @staticmethod
    def quiz_to_model(entity: AssessmentEntity) -> AssessmentQuiz:
        questions_ids = [q.question_id for q in entity.questions]
        assessment_quiz = AssessmentQuiz(
            assessment_id=entity.id,
            user_id=entity.user_id,
            created_at=entity.created_at,
            questions=questions_ids,
        )
        return assessment_quiz

    @staticmethod
    def answer_to_entity(answer: AssessmentAnswer) -> AssessmentAnswerEntity:
        return AssessmentAnswerEntity(
            assessment_id=answer.assessment_id,
            question_id=answer.question_id,
            answer=answer.answer,
            time_taken_seconds=answer.time_taken_seconds,
        )


class SqlliteAssessmentAnswerMapper:
    @staticmethod
    def to_entity(request: AssessmentAnswer) -> AssessmentAnswerEntity:
        return AssessmentAnswerEntity(
            assessment_id=request.assessment_id,
            question_id=request.question_id,
            answer=request.answer,
            time_taken_seconds=request.time_taken_seconds,
        )

    @staticmethod
    def to_model(entity: AssessmentAnswerEntity) -> AssessmentAnswer:
        return AssessmentAnswer(
            assessment_id=entity.assessment_id,
            question_id=entity.question_id,
            answer=entity.answer,
            time_taken_seconds=entity.time_taken_seconds,
        )
