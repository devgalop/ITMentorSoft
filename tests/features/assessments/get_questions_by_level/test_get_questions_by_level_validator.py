from src.features.assessments.get_questions_by_level.get_questions_by_level_request import (
    GetQuestionsByLevelRequest,
)
import pytest

VALID_DIFFICULTY = "básico"


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetQuestionsByLevelRequest(difficulty=VALID_DIFFICULTY)
    assert request.difficulty == VALID_DIFFICULTY


def test_when_difficulty_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Difficulty cannot be empty"):
        GetQuestionsByLevelRequest(difficulty="")


def test_when_difficulty_is_invalid_then_exception_is_raised():
    with pytest.raises(ValueError, match="Invalid difficulty"):
        GetQuestionsByLevelRequest(difficulty="invalid")


def test_when_difficulty_is_intermedio_then_exception_is_not_raised():
    request = GetQuestionsByLevelRequest(difficulty="intermedio")
    assert request.difficulty == "intermedio"


def test_when_difficulty_is_avanzado_then_exception_is_not_raised():
    request = GetQuestionsByLevelRequest(difficulty="avanzado")
    assert request.difficulty == "avanzado"
