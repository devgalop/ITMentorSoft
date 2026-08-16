import pytest

from src.features.assessments.get_assessment_result.get_assessment_result_request import (
    GetAssessmentResultRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = GetAssessmentResultRequest(
        assessment_id="assessment_12345", user_id="user_67890"
    )
    assert request.assessment_id == "assessment_12345"
    assert request.user_id == "user_67890"


def test_when_assessment_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="assessment_id must not be empty"):
        GetAssessmentResultRequest(assessment_id="", user_id="user_67890")


def test_when_assessment_id_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="assessment_id must be at least 5 characters long"
    ):
        GetAssessmentResultRequest(assessment_id="ass", user_id="user_67890")


def test_when_assessment_id_is_too_long_should_raise_exception():
    long_id = "a" * 101
    with pytest.raises(
        ValueError, match="assessment_id must not exceed 100 characters"
    ):
        GetAssessmentResultRequest(assessment_id=long_id, user_id="user_67890")


def test_when_assessment_id_is_exactly_5_characters_should_not_raise():
    request = GetAssessmentResultRequest(assessment_id="ass12", user_id="user_67890")
    assert request.assessment_id == "ass12"


def test_when_assessment_id_is_exactly_100_characters_should_not_raise():
    valid_id = "a" * 100
    request = GetAssessmentResultRequest(assessment_id=valid_id, user_id="user_67890")
    assert request.assessment_id == valid_id


def test_when_user_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="user_id must not be empty"):
        GetAssessmentResultRequest(assessment_id="assessment_12345", user_id="")


def test_when_user_id_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="user_id must be at least 5 characters long"):
        GetAssessmentResultRequest(assessment_id="assessment_12345", user_id="usr")


def test_when_user_id_is_too_long_should_raise_exception():
    long_id = "u" * 101
    with pytest.raises(ValueError, match="user_id must not exceed 100 characters"):
        GetAssessmentResultRequest(assessment_id="assessment_12345", user_id=long_id)


def test_when_user_id_is_exactly_5_characters_should_not_raise():
    request = GetAssessmentResultRequest(
        assessment_id="assessment_12345", user_id="usr12"
    )
    assert request.user_id == "usr12"


def test_when_user_id_is_exactly_100_characters_should_not_raise():
    valid_id = "u" * 100
    request = GetAssessmentResultRequest(
        assessment_id="assessment_12345", user_id=valid_id
    )
    assert request.user_id == valid_id
