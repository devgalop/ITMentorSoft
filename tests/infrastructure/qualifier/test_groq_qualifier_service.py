import json
from unittest.mock import MagicMock, patch

import pytest

from src.features.assessments.shared.assessment import AssessmentAnswer
from src.features.assessments.shared.qualifier_service import (
    BatchQualificationError,
    BatchQualifierPrompt,
)
from src.features.assessments.shared.question import QuestionBuilder
from src.infrastructure.qualifier.groq_qualifier_service import (
    GroqQualifierService,
)


def _make_rubric(question_id: str) -> QuestionBuilder:
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


def _make_batch_prompt(count: int = 2):
    rubrics = [_make_rubric(f"q-{i:03d}") for i in range(1, count + 1)]
    answers = [_make_answer(f"a-{i:03d}", f"q-{i:03d}") for i in range(1, count + 1)]
    prompt = BatchQualifierPrompt(
        rubrics=rubrics,
        answers=answers,
        qualifier_mode="normal",
        user_id="user-001",
        assessment_id="assess-001",
    )
    return prompt, rubrics, answers


def _make_json_result(answer_id: str, score: int = 80) -> dict:
    return {
        "answer_id": answer_id,
        "score": score,
        "feedback": "Good answer",
        "key_concepts_detected": ["concept1"],
        "misconceptions_detected": [],
    }


class TestGroqBatchQualification:
    """Tests for GroqQualifierService.qualify_batch."""

    @pytest.fixture
    def service(self):
        """Create a service with a mocked Groq client."""
        with patch(
            "src.infrastructure.qualifier.groq_qualifier_service.Groq"
        ) as mock_groq:
            mock_client = MagicMock()
            mock_groq.return_value = mock_client
            svc = GroqQualifierService()
            svc.client = mock_client
            return svc

    @pytest.mark.asyncio
    async def test_valid_json_array_returns_results(self, service):
        """GIVEN valid batch JSON response
        WHEN qualify_batch is called
        THEN results are returned in input order.
        """
        prompt, rubrics, answers = _make_batch_prompt(3)

        llm_response = json.dumps(
            [
                _make_json_result("a-003", 90),
                _make_json_result("a-001", 80),
                _make_json_result("a-002", 85),
            ]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        results = await service.qualify_batch(prompt)

        assert len(results) == 3
        assert results[0].answer_id == "a-001"
        assert results[0].score == 80
        assert results[1].answer_id == "a-002"
        assert results[1].score == 85
        assert results[2].answer_id == "a-003"
        assert results[2].score == 90

    @pytest.mark.asyncio
    async def test_think_tags_stripped_before_json_parse(self, service):
        """GIVEN LLM response contains <think>...</think> tags before JSON
        WHEN qualify_batch is called
        THEN tags are stripped and JSON is parsed successfully.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        llm_response = (
            "<think>Let me analyze these answers carefully...</think>\n"
            + json.dumps(
                [
                    _make_json_result("a-001", 75),
                    _make_json_result("a-002", 85),
                ]
            )
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        results = await service.qualify_batch(prompt)

        assert len(results) == 2
        assert results[0].answer_id == "a-001"
        assert results[0].score == 75

    @pytest.mark.asyncio
    async def test_malformed_json_raises_batch_qualification_error(self, service):
        """GIVEN LLM returns non-JSON response
        WHEN qualify_batch is called
        THEN BatchQualificationError is raised.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "not json"
        service.client.chat.completions.create.return_value = mock_completion

        with pytest.raises(BatchQualificationError):
            await service.qualify_batch(prompt)

    @pytest.mark.asyncio
    async def test_llm_called_once(self, service):
        """GIVEN a batch prompt
        WHEN qualify_batch is called
        THEN exactly one Groq API call is made.
        """
        prompt, rubrics, answers = _make_batch_prompt(5)

        llm_response = json.dumps(
            [_make_json_result(f"a-{i:03d}", 80) for i in range(1, 6)]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        await service.qualify_batch(prompt)

        service.client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_orphan_result_discarded(self, service):
        """GIVEN LLM returns result with unknown answer_id
        WHEN qualify_batch is called
        THEN orphan result is discarded.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        llm_response = json.dumps(
            [
                _make_json_result("a-001", 80),
                _make_json_result("a-999", 70),
                _make_json_result("a-002", 85),
            ]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        with patch(
            "src.infrastructure.qualifier.groq_qualifier_service.logger"
        ) as mock_logger:
            results = await service.qualify_batch(prompt)

        assert len(results) == 2
        result_ids = [r.answer_id for r in results]
        assert "a-999" not in result_ids
        mock_logger.warning.assert_called_once()
