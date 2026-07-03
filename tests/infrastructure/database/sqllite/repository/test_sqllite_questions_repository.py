from unittest.mock import AsyncMock, MagicMock

import pytest

from src.features.assessments.shared.question import (
    Question,
    QuestionDifficulty,
    QuestionStatus,
)
from src.infrastructure.database.sqllite.models.sqllite_question_mapper import (
    SqlliteQuestionMapper,
)
from src.infrastructure.database.sqllite.models.sqllite_question_model import (
    QuestionEntity,
    QuestionRubricScoreEntity,
)
from src.infrastructure.database.sqllite.repository.sqllite_questions_repository import (
    SqlliteQuestionsRepository,
)


def _make_question_entity(
    question_id: str, text: str = "Test question", with_rubric: bool = True
) -> QuestionEntity:
    """Create a QuestionEntity for testing."""
    entity = QuestionEntity(
        id=question_id,
        text=text,
        concept="Test concept",
        definition="Test definition",
        simple_explanation="Test explanation",
        correct_sample="Correct",
        wrong_sample="Wrong",
        difficulty=QuestionDifficulty.EASY.value,
        classification="Test category",
        version=1,
        common_misconceptions="",
        semantic_keywords="",
        status=QuestionStatus.PUBLISHED.value,
    )
    if with_rubric:
        entity.rubric = [
            QuestionRubricScoreEntity(
                score=100, explanation="Excellent", question=entity
            ),
            QuestionRubricScoreEntity(score=50, explanation="Partial", question=entity),
        ]
    else:
        entity.rubric = []
    return entity


def _make_repository(session_factory, mapper=None):
    """Create a SqlliteQuestionsRepository with the given session factory."""
    return SqlliteQuestionsRepository(
        session_factory=session_factory, mapper=mapper or SqlliteQuestionMapper
    )


class TestGetQuestionRubricsBulk:
    """Tests for get_question_rubrics_bulk — bulk rubric fetching."""

    @pytest.mark.asyncio
    async def test_when_empty_list_then_returns_empty_dict(self):
        """GIVEN an empty list of question IDs
        WHEN get_question_rubrics_bulk is called
        THEN the method returns an empty dictionary.
        """
        mock_session = AsyncMock()
        repo = _make_repository(mock_session)

        result = await repo.get_question_rubrics_bulk([])

        assert result == {}
        mock_session.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_when_all_rubrics_present_then_returns_dict_with_all_questions(self):
        """GIVEN a list of 3 question IDs that all exist in the database
        WHEN get_question_rubrics_bulk is called
        THEN the method returns dict[str, Question] with 3 entries
        AND each Question object contains its full rubric.
        """
        q1 = _make_question_entity("q-001", "Question 1")
        q2 = _make_question_entity("q-002", "Question 2")
        q3 = _make_question_entity("q-003", "Question 3")

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [q1, q2, q3]

        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_result

        repo = _make_repository(mock_session)
        question_ids = ["q-001", "q-002", "q-003"]

        result = await repo.get_question_rubrics_bulk(question_ids)

        assert len(result) == 3
        assert "q-001" in result
        assert "q-002" in result
        assert "q-003" in result
        assert isinstance(result["q-001"], Question)
        assert len(result["q-001"].rubric) == 2
        assert result["q-001"].rubric[0].score == 100
        assert result["q-002"].rubric[0].score == 100
        assert result["q-003"].rubric[0].score == 100

    @pytest.mark.asyncio
    async def test_when_some_missing_then_returns_only_existing(self):
        """GIVEN a list of question IDs where some do not exist
        WHEN get_question_rubrics_bulk is called
        THEN only existing questions are included in the returned dictionary
        AND missing question IDs are omitted from the result (not raised as error).
        """
        q1 = _make_question_entity("q-001", "Question 1")
        q3 = _make_question_entity("q-003", "Question 3")

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [q1, q3]

        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_result

        repo = _make_repository(mock_session)
        question_ids = ["q-001", "q-002-missing", "q-003"]

        result = await repo.get_question_rubrics_bulk(question_ids)

        assert len(result) == 2
        assert "q-001" in result
        assert "q-003" in result
        assert "q-002-missing" not in result

    @pytest.mark.asyncio
    async def test_uses_single_query_with_in_clause(self):
        """GIVEN a list of question IDs
        WHEN get_question_rubrics_bulk is called
        THEN exactly one SQL query is executed with an IN clause.
        """
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []

        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_result

        repo = _make_repository(mock_session)
        question_ids = ["q-001", "q-002", "q-003"]

        await repo.get_question_rubrics_bulk(question_ids)

        mock_session.execute.assert_called_once()
        call_args = mock_session.execute.call_args[0][0]
        # Verify the statement uses an IN clause
        compiled = str(call_args.compile())
        assert "IN" in compiled.upper() or "in" in compiled.lower()
