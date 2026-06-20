from src.features.assessments.shared.assessment import (
    Assessment,
    AssessmentAnswer,
    AssessmentQuiz,
)
from src.features.assessments.shared.qualifier_service import QualifierResult
from src.infrastructure.database.sqllite.models.sqllite_assessment_model import (
    AssessmentAnswerEntity,
    AssessmentEntity,
    AssessmentMisconceptionEntity,
    AssessmentQualificationEntity,
    AssessmentQualificationKeyConceptEntity,
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
        return SqlliteAssessmentAnswerMapper.to_entity(answer)

    @staticmethod
    def qualifier_result_to_entity(
        qualifier_result: QualifierResult,
    ) -> AssessmentQualificationEntity:
        return SqlliteAssessmentQualificationMapper.to_entity(qualifier_result)

    @staticmethod
    def qualifier_result_key_concept_to_entity(
        qualification_id: str, key_concept: str
    ) -> AssessmentQualificationKeyConceptEntity:
        return SqlliteAssessmentQualificationMapper.to_key_concepts_entity(
            qualification_id, key_concept
        )

    @staticmethod
    def qualifier_result_misconception_to_entity(
        qualification_id: str, misconception: str
    ) -> AssessmentMisconceptionEntity:
        return SqlliteAssessmentQualificationMapper.to_misconceptions_entity(
            qualification_id, misconception
        )


class SqlliteAssessmentAnswerMapper:
    @staticmethod
    def to_entity(request: AssessmentAnswer) -> AssessmentAnswerEntity:
        return AssessmentAnswerEntity(
            id=request.answer_id,
            assessment_id=request.assessment_id,
            question_id=request.question_id,
            answer=request.answer,
            time_taken_seconds=request.time_taken_seconds,
        )

    @staticmethod
    def to_model(entity: AssessmentAnswerEntity) -> AssessmentAnswer:
        return AssessmentAnswer(
            answer_id=entity.id,
            assessment_id=entity.assessment_id,
            question_id=entity.question_id,
            answer=entity.answer,
            time_taken_seconds=entity.time_taken_seconds,
        )


class SqlliteAssessmentQualificationMapper:
    @staticmethod
    def to_entity(model: QualifierResult) -> AssessmentQualificationEntity:
        return AssessmentQualificationEntity(
            id=model.id,
            assessment_id=model.assessment_id,
            question_id=model.question_id,
            user_id=model.user_id,
            answer_id=model.answer_id,
            score=model.score,
            feedback=model.feedback,
            question_topic=model.question_topic,
            question_difficulty=model.question_difficulty,
        )

    @staticmethod
    def to_key_concepts_entity(
        qualification_id: str, key_concept: str
    ) -> AssessmentQualificationKeyConceptEntity:
        return AssessmentQualificationKeyConceptEntity(
            qualification_id=qualification_id, key_concept=key_concept
        )

    @staticmethod
    def to_misconceptions_entity(
        qualification_id: str, misconception: str
    ) -> AssessmentMisconceptionEntity:
        return AssessmentMisconceptionEntity(
            qualification_id=qualification_id, misconception=misconception
        )

    @staticmethod
    def to_model(entity: AssessmentQualificationEntity) -> QualifierResult:
        key_concepts = [kc.key_concept for kc in entity.key_concepts]
        misconceptions = [mc.misconception for mc in entity.misconceptions]
        return QualifierResult(
            id=entity.id,
            question_id=entity.question_id,
            user_id=entity.user_id,
            score=entity.score,
            feedback=entity.feedback,
            key_concepts_detected=key_concepts,
            misconceptions_detected=misconceptions,
            question_topic=entity.question_topic,
            assessment_id=entity.assessment_id,
            question_difficulty=entity.question_difficulty,
            answer_id=entity.answer_id,
        )
