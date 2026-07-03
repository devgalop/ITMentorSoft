from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.features.assessments.evaluate.evaluate_assessment_service import (
    EvaluateAssessmentService,
)
from src.features.assessments.shared.assessment import (
    Assessment,
    AssessmentAnswer,
)
from src.features.assessments.shared.question import (
    Question,
    QuestionBuilder,
)
from src.features.assessments.shared.qualifier_service import (
    QualifierResult,
    QualifierService,
)
from src.features.assessments.shared.questions_repository import QuestionRepository


def _make_assessment(answers: list[AssessmentAnswer]) -> Assessment:
    return Assessment(
        assessment_id="assess-001",
        user_id="user-001",
        created_at=datetime.now(),
        answers=answers,
    )


def _make_answer(
    answer_id: str, question_id: str, answer_text: str = "Test answer"
) -> AssessmentAnswer:
    return AssessmentAnswer(
        answer_id=answer_id,
        assessment_id="assess-001",
        question_id=question_id,
        answer=answer_text,
        time_taken_seconds=30,
    )


def _make_rubric(question_id: str) -> Question:
    return (
        QuestionBuilder()
        .set_question_id(question_id)
        .set_text_to_evaluate(f"Question: {question_id}")
        .set_concept("Test concept")
        .set_definition("Test definition")
        .set_simple_explanation("Test explanation")
        .set_correct_sample("Correct")
        .set_wrong_sample("Wrong")
        .add_rubric(100, "Excellent")
        .add_rubric(50, "Partial")
        .build()
    )


def _make_qualifier_result(answer_id: str, question_id: str) -> QualifierResult:
    return QualifierResult(
        id=f"result-{answer_id}",
        question_id=question_id,
        user_id="user-001",
        score=85,
        feedback="Good answer",
        key_concepts_detected=["concept1"],
        misconceptions_detected=[],
        question_topic="Test topic",
        assessment_id="assess-001",
        question_difficulty="básico",
        answer_id=answer_id,
    )


class TestQualifyAssessmentBulkFetch:
    """Tests for refactored qualify_assessment using bulk rubric fetching."""

    @pytest.mark.asyncio
    async def test_when_all_rubrics_exist_then_bulk_fetch_called_once(self):
        """GIVEN an assessment with 3 answers and all rubrics exist
        WHEN qualify_assessment is called
        THEN get_question_rubrics_bulk is called exactly once with all question IDs.
        """
        answers = [
            _make_answer("a-001", "q-001"),
            _make_answer("a-002", "q-002"),
            _make_answer("a-003", "q-003"),
        ]
        assessment = _make_assessment(answers)

        rubrics = {
            "q-001": _make_rubric("q-001"),
            "q-002": _make_rubric("q-002"),
            "q-003": _make_rubric("q-003"),
        }

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value=rubrics)

        qualifier_service = AsyncMock(spec=QualifierService)
        qualifier_service.qualify = AsyncMock(
            side_effect=lambda prompt: _make_qualifier_result(
                prompt.answer_id, prompt.rubric.question_id
            )
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )

        results = await service.qualify_assessment(assessment)

        question_repo.get_question_rubrics_bulk.assert_called_once_with(
            ["q-001", "q-002", "q-003"]
        )
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_when_all_rubrics_exist_then_per_answer_fetch_not_called(self):
        """GIVEN an assessment with answers
        WHEN qualify_assessment is called
        THEN get_question_rubric (per-answer) is NOT called — only bulk fetch is used.
        """
        answers = [_make_answer("a-001", "q-001")]
        assessment = _make_assessment(answers)

        rubrics = {"q-001": _make_rubric("q-001")}

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value=rubrics)
        question_repo.get_question_rubric = AsyncMock()

        qualifier_service = AsyncMock(spec=QualifierService)
        qualifier_service.qualify = AsyncMock(
            side_effect=lambda prompt: _make_qualifier_result(
                prompt.answer_id, prompt.rubric.question_id
            )
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )

        await service.qualify_assessment(assessment)

        question_repo.get_question_rubric.assert_not_called()

    @pytest.mark.asyncio
    async def test_when_some_rubrics_missing_then_those_answers_are_skipped(self):
        """GIVEN an assessment where some question_ids have no rubric
        WHEN qualify_assessment is called
        THEN those answers are silently skipped
        AND only answers with rubrics are sent to the qualifier.
        """
        answers = [
            _make_answer("a-001", "q-001"),
            _make_answer("a-002", "q-002-missing"),
            _make_answer("a-003", "q-003"),
        ]
        assessment = _make_assessment(answers)

        rubrics = {
            "q-001": _make_rubric("q-001"),
            "q-003": _make_rubric("q-003"),
        }

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value=rubrics)

        qualifier_service = AsyncMock(spec=QualifierService)
        qualifier_service.qualify = AsyncMock(
            side_effect=lambda prompt: _make_qualifier_result(
                prompt.answer_id, prompt.rubric.question_id
            )
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )

        results = await service.qualify_assessment(assessment)

        assert len(results) == 2
        assert qualifier_service.qualify.call_count == 2

    @pytest.mark.asyncio
    async def test_uses_dict_lookup_for_each_answer(self):
        """GIVEN an assessment with multiple answers
        WHEN qualify_assessment is called
        THEN each answer's rubric is looked up via dict.get(answer.question_id).
        """
        answers = [
            _make_answer("a-001", "q-001"),
            _make_answer("a-002", "q-002"),
        ]
        assessment = _make_assessment(answers)

        rubrics = {
            "q-001": _make_rubric("q-001"),
            "q-002": _make_rubric("q-002"),
        }

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value=rubrics)

        qualifier_service = AsyncMock(spec=QualifierService)
        qualifier_service.qualify = AsyncMock(
            side_effect=lambda prompt: _make_qualifier_result(
                prompt.answer_id, prompt.rubric.question_id
            )
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )

        await service.qualify_assessment(assessment)

        # Verify each qualifier call received the correct rubric
        calls = qualifier_service.qualify.call_args_list
        assert len(calls) == 2
        # First call should have q-001 rubric
        assert calls[0][0][0].rubric.question_id == "q-001"
        assert calls[0][0][0].answer_id == "a-001"
        # Second call should have q-002 rubric
        assert calls[1][0][0].rubric.question_id == "q-002"
        assert calls[1][0][0].answer_id == "a-002"

    @pytest.mark.asyncio
    async def test_when_empty_assessment_then_returns_empty_list(self):
        """GIVEN an assessment with no answers
        WHEN qualify_assessment is called
        THEN an empty list is returned.
        """
        assessment = _make_assessment([])

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value={})

        qualifier_service = AsyncMock(spec=QualifierService)

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )

        results = await service.qualify_assessment(assessment)

        assert results == []
        question_repo.get_question_rubrics_bulk.assert_not_called()
