from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.features.assessments.evaluate.evaluate_assessment_service import (
    EvaluateAssessmentService,
    _validate_chunk_size,
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
    BatchQualificationError,
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
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=lambda prompt: [
                _make_qualifier_result(a.answer_id, a.question_id)
                for a in prompt.answers
            ]
        )
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
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=lambda prompt: [
                _make_qualifier_result(a.answer_id, a.question_id)
                for a in prompt.answers
            ]
        )
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
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=lambda prompt: [
                _make_qualifier_result(a.answer_id, a.question_id)
                for a in prompt.answers
            ]
        )
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
        assert qualifier_service.qualify.call_count == 0

    @pytest.mark.asyncio
    async def test_uses_dict_lookup_for_each_answer(self):
        """GIVEN an assessment with multiple answers
        WHEN qualify_assessment is called
        THEN each answer's rubric is included in the batch prompt.
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
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=lambda prompt: [
                _make_qualifier_result(a.answer_id, a.question_id)
                for a in prompt.answers
            ]
        )
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

        # Verify batch call received both rubrics
        calls = qualifier_service.qualify_batch.call_args_list
        assert len(calls) == 1
        batch_prompt = calls[0][0][0]
        assert len(batch_prompt.rubrics) == 2
        assert batch_prompt.rubrics[0].question_id == "q-001"
        assert batch_prompt.answers[0].answer_id == "a-001"
        assert batch_prompt.rubrics[1].question_id == "q-002"
        assert batch_prompt.answers[1].answer_id == "a-002"

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


class TestChunkSizeValidation:
    """Tests for ASSESSMENT_QUALIFICATION_CHUNK_SIZE validation."""

    def test_default_value_is_10(self):
        """GIVEN no env var set
        WHEN _validate_chunk_size is called with None
        THEN returns 10.
        """
        assert _validate_chunk_size(None) == 10

    def test_custom_valid_value(self):
        """GIVEN env var set to "5"
        WHEN _validate_chunk_size is called
        THEN returns 5.
        """
        assert _validate_chunk_size("5") == 5

    def test_negative_value_raises_value_error(self):
        """GIVEN env var set to "-2"
        WHEN _validate_chunk_size is called
        THEN ValueError is raised.
        """
        with pytest.raises(ValueError, match="positive integer"):
            _validate_chunk_size("-2")

    def test_zero_raises_value_error(self):
        """GIVEN env var set to "0"
        WHEN _validate_chunk_size is called
        THEN ValueError is raised.
        """
        with pytest.raises(ValueError, match="positive integer"):
            _validate_chunk_size("0")

    def test_non_numeric_raises_value_error(self):
        """GIVEN env var set to "abc"
        WHEN _validate_chunk_size is called
        THEN ValueError is raised.
        """
        with pytest.raises(ValueError, match="positive integer"):
            _validate_chunk_size("abc")

    def test_float_string_raises_value_error(self):
        """GIVEN env var set to "3.5"
        WHEN _validate_chunk_size is called
        THEN ValueError is raised.
        """
        with pytest.raises(ValueError, match="positive integer"):
            _validate_chunk_size("3.5")


class TestQualifyAssessmentChunking:
    """Tests for chunking logic in qualify_assessment."""

    @pytest.mark.asyncio
    async def test_25_answers_chunk_size_10_makes_3_batch_calls(self):
        """GIVEN an assessment with 25 answers and chunk_size=10
        WHEN qualify_assessment is called
        THEN exactly 3 calls to qualify_batch are made (10 + 10 + 5).
        """
        answers = [_make_answer(f"a-{i:03d}", f"q-{i:03d}") for i in range(1, 26)]
        assessment = _make_assessment(answers)

        rubrics = {f"q-{i:03d}": _make_rubric(f"q-{i:03d}") for i in range(1, 26)}

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value=rubrics)

        qualifier_service = AsyncMock(spec=QualifierService)
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=lambda prompt: [
                _make_qualifier_result(a.answer_id, a.question_id)
                for a in prompt.answers
            ]
        )
        qualifier_service.qualify = AsyncMock()

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )
        service.chunk_size = 10

        results = await service.qualify_assessment(assessment)

        assert qualifier_service.qualify_batch.call_count == 3
        assert len(results) == 25

    @pytest.mark.asyncio
    async def test_3_answers_fits_in_one_chunk(self):
        """GIVEN an assessment with 3 answers and chunk_size=10
        WHEN qualify_assessment is called
        THEN exactly 1 call to qualify_batch is made.
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
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=lambda prompt: [
                _make_qualifier_result(a.answer_id, a.question_id)
                for a in prompt.answers
            ]
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )
        service.chunk_size = 10

        results = await service.qualify_assessment(assessment)

        assert qualifier_service.qualify_batch.call_count == 1
        assert len(results) == 3


class TestQualifyAssessmentFallback:
    """Tests for fallback to per-item qualify when batch fails."""

    @pytest.mark.asyncio
    async def test_batch_fails_then_per_item_qualify_called_for_chunk(self):
        """GIVEN qualify_batch raises BatchQualificationError
        WHEN qualify_assessment is called
        THEN per-item qualify is called as fallback for that chunk.
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
        # Batch always fails
        qualifier_service.qualify_batch = AsyncMock(
            side_effect=BatchQualificationError(raw_response="bad json")
        )
        # Per-item works
        qualifier_service.qualify = AsyncMock(
            side_effect=lambda prompt: _make_qualifier_result(
                prompt.answer_id, prompt.rubric.question_id
            )
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )
        service.chunk_size = 10

        results = await service.qualify_assessment(assessment)

        # Fallback: per-item qualify called for each answer
        assert qualifier_service.qualify.call_count == 2
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_batch_partial_fallback_only_for_failed_chunk(self):
        """GIVEN first chunk batch succeeds but second chunk fails
        WHEN qualify_assessment is called
        THEN first chunk results are kept and second chunk uses per-item fallback.
        """
        answers = [_make_answer(f"a-{i:03d}", f"q-{i:03d}") for i in range(1, 16)]
        assessment = _make_assessment(answers)

        rubrics = {f"q-{i:03d}": _make_rubric(f"q-{i:03d}") for i in range(1, 16)}

        question_repo = AsyncMock(spec=QuestionRepository)
        question_repo.get_question_rubrics_bulk = AsyncMock(return_value=rubrics)

        call_count = 0

        async def mock_qualify_batch(prompt):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First chunk succeeds
                return [
                    _make_qualifier_result(a.answer_id, a.question_id)
                    for a in prompt.answers
                ]
            else:
                # Second chunk fails
                raise BatchQualificationError(raw_response="bad")

        qualifier_service = AsyncMock(spec=QualifierService)
        qualifier_service.qualify_batch = AsyncMock(side_effect=mock_qualify_batch)
        qualifier_service.qualify = AsyncMock(
            side_effect=lambda prompt: _make_qualifier_result(
                prompt.answer_id, prompt.rubric.question_id
            )
        )

        assessment_repo = AsyncMock()

        service = EvaluateAssessmentService(
            assessment_repo, qualifier_service, question_repo
        )
        service.chunk_size = 10

        results = await service.qualify_assessment(assessment)

        # First chunk: 10 results from batch
        # Second chunk: 5 results from fallback
        assert len(results) == 15
        assert qualifier_service.qualify_batch.call_count == 2
        assert qualifier_service.qualify.call_count == 5  # 5 answers in second chunk
