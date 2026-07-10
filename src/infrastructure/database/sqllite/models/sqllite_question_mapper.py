from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    Question,
    QuestionDifficulty,
    QuestionReview,
    QuestionRubricScore,
    QuestionStatus,
)
from src.features.assessments.shared.question_details import (
    QuestionDetails,
    RubricScore,
)
from src.infrastructure.database.sqllite.models.sqllite_question_model import (
    QuestionEntity,
    QuestionReviewEntity,
    QuestionRubricScoreEntity,
)

PIPE_SEPARATOR = "|"


class SqlliteQuestionMapper:

    @staticmethod
    def to_evaluative_model(question: QuestionEntity) -> EvaluativeQuestion:
        return EvaluativeQuestion(
            question_id=question.id,
            text_to_evaluate=question.text,
            topic=question.classification,
        )

    @staticmethod
    def to_model(question: QuestionEntity) -> Question:
        rubric = [
            SqlliteQuestionMapper.to_rubric_score_model(r) for r in question.rubric
        ]
        model = Question(
            text_to_evaluate=question.text,
            concept=question.concept,
            definition=question.definition,
            simple_explanation=question.simple_explanation,
            correct_sample=question.correct_sample,
            wrong_sample=question.wrong_sample,
            common_misconception=(
                question.common_misconceptions.split(PIPE_SEPARATOR)
                if question.common_misconceptions
                else []
            ),
            rubric=rubric,
            semantic_keywords=(
                question.semantic_keywords.split(PIPE_SEPARATOR)
                if question.semantic_keywords
                else []
            ),
            status=QuestionStatus(question.status),
            difficulty=QuestionDifficulty(question.difficulty),
            classification=question.classification,
            version=question.version,
        )
        model.update_question_id(question.id)
        return model

    @staticmethod
    def to_detailed_model(question: QuestionEntity) -> QuestionDetails:
        rubric = [
            SqlliteQuestionMapper.to_rubric_score_response(r) for r in question.rubric
        ]
        model = QuestionDetails(
            question_id=question.id,
            text_to_evaluate=question.text,
            concept=question.concept,
            definition=question.definition,
            simple_explanation=question.simple_explanation,
            correct_sample=question.correct_sample,
            wrong_sample=question.wrong_sample,
            common_misconceptions=(
                question.common_misconceptions.split(PIPE_SEPARATOR)
                if question.common_misconceptions
                else []
            ),
            rubric=rubric,
            semantic_keywords=(
                question.semantic_keywords.split(PIPE_SEPARATOR)
                if question.semantic_keywords
                else []
            ),
            status=question.status,
            difficulty=question.difficulty,
            classification=question.classification,
            version=question.version,
        )
        return model

    @staticmethod
    def to_review_entity(review: QuestionReview) -> QuestionReviewEntity:
        return QuestionReviewEntity(
            id=review.review_id,
            question_id=review.question_id,
            reviewer_id=review.reviewer_id,
            review_comments=review.review_comments,
        )

    @staticmethod
    def to_rubric_score_model(
        rubric_score: QuestionRubricScoreEntity,
    ) -> QuestionRubricScore:
        return QuestionRubricScore(
            score=rubric_score.score, explanation=rubric_score.explanation
        )

    @staticmethod
    def to_rubric_score_response(
        rubric_score: QuestionRubricScoreEntity,
    ) -> RubricScore:
        return RubricScore(
            score=rubric_score.score, explanation=rubric_score.explanation
        )

    @staticmethod
    def to_entity(question: Question) -> QuestionEntity:
        return QuestionEntity(
            id=question.question_id,
            text=question.text_to_evaluate,
            concept=question.concept,
            definition=question.definition,
            simple_explanation=question.simple_explanation,
            correct_sample=question.correct_sample,
            wrong_sample=question.wrong_sample,
            common_misconceptions=PIPE_SEPARATOR.join(question.common_misconception),
            semantic_keywords=PIPE_SEPARATOR.join(question.semantic_keywords),
            status=question.status.value,
            difficulty=question.difficulty.value,
            classification=question.classification,
            version=question.version,
        )

    @staticmethod
    def to_rubric_score_entity(
        question_id: str, rubric_score: QuestionRubricScore
    ) -> QuestionRubricScoreEntity:
        return QuestionRubricScoreEntity(
            question_id=question_id,
            score=rubric_score.score,
            explanation=rubric_score.explanation,
        )

    @staticmethod
    def to_rubric_score_entities(
        question_id: str, rubric_scores: list[QuestionRubricScore]
    ) -> list[QuestionRubricScoreEntity]:
        return [
            SqlliteQuestionMapper.to_rubric_score_entity(question_id, r)
            for r in rubric_scores
        ]
