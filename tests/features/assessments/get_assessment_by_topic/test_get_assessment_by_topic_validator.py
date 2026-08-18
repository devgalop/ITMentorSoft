from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_request import (
    GetAssessmentByTopicRequest,
)
import pytest

VALID_STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
VALID_TOPIC_ID = "topic-a1b2c3d4e5f6a7b8c9d0e1f2"


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetAssessmentByTopicRequest(
        topic_id=VALID_TOPIC_ID,
        student_id=VALID_STUDENT_ID,
    )
    assert request.topic_id == VALID_TOPIC_ID
    assert request.student_id == VALID_STUDENT_ID


def test_when_topic_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Topic ID must not be empty"):
        GetAssessmentByTopicRequest(
            topic_id="",
            student_id=VALID_STUDENT_ID,
        )


def test_when_topic_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Topic ID must not exceed 100 characters"):
        GetAssessmentByTopicRequest(
            topic_id="a" * 101,
            student_id=VALID_STUDENT_ID,
        )


def test_when_topic_id_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Topic ID must be at least 5 characters long"):
        GetAssessmentByTopicRequest(
            topic_id="abc",
            student_id=VALID_STUDENT_ID,
        )


def test_when_student_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Student ID must not be empty"):
        GetAssessmentByTopicRequest(
            topic_id=VALID_TOPIC_ID,
            student_id="",
        )


def test_when_student_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Student ID must not exceed 100 characters"):
        GetAssessmentByTopicRequest(
            topic_id=VALID_TOPIC_ID,
            student_id="a" * 101,
        )


def test_when_student_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Student ID must be at least 5 characters long"
    ):
        GetAssessmentByTopicRequest(
            topic_id=VALID_TOPIC_ID,
            student_id="abc",
        )
