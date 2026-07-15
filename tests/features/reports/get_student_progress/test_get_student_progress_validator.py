from src.features.reports.get_student_progress.get_student_progress_request import (
    GetStudentProgressRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetStudentProgressRequest(student_id="123e4567e89b12d3a456426614174000")
    assert request.student_id == "123e4567e89b12d3a456426614174000"


def test_when_student_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="student_id must not be empty"):
        GetStudentProgressRequest(student_id="")


def test_when_student_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="student_id must be at least 5 characters long"
    ):
        GetStudentProgressRequest(student_id="abcd")


def test_when_student_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="student_id must not exceed 100 characters"):
        GetStudentProgressRequest(student_id="a" * 101)
