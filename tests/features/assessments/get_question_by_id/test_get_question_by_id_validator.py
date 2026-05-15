from src.features.assessments.get_question_by_id.get_question_by_id_request import (
    GetQuestionByIdRequest,
)
import pytest

VALID_QUESTION_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetQuestionByIdRequest(question_id=VALID_QUESTION_ID)
    assert request.question_id == VALID_QUESTION_ID


def test_when_question_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Question ID cannot be empty"):
        GetQuestionByIdRequest(question_id="")


def test_when_question_id_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Question ID cannot be longer than 32 characters"
    ):
        GetQuestionByIdRequest(question_id="a" * 33)


def test_when_question_id_is_not_alphanumeric_then_exception_is_raised():
    with pytest.raises(ValueError, match="Question ID must be alphanumeric"):
        GetQuestionByIdRequest(question_id="abc-123")
