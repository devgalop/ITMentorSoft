from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
import pytest

VALID_STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetAssessmentRequest(number_of_questions=10, student_id=VALID_STUDENT_ID)
    assert request.number_of_questions == 10
    assert request.student_id == VALID_STUDENT_ID


def test_when_number_of_questions_is_zero_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Number of questions must be a positive integer"
    ):
        GetAssessmentRequest(number_of_questions=0, student_id=VALID_STUDENT_ID)


def test_when_number_of_questions_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Number of questions must be a positive integer"
    ):
        GetAssessmentRequest(number_of_questions=-5, student_id=VALID_STUDENT_ID)


def test_when_student_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Student ID must not be empty"):
        GetAssessmentRequest(number_of_questions=10, student_id="")


def test_when_student_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Student ID must not exceed 100 characters"):
        GetAssessmentRequest(number_of_questions=10, student_id="a" * 101)


def test_when_student_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Student ID must be at least 5 characters long"
    ):
        GetAssessmentRequest(number_of_questions=10, student_id="abc")
