import pytest

from src.features.assessments.get_qualification_status.get_qualification_status_request import (
    GetQualificationStatusRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = GetQualificationStatusRequest(
        user_id="user_12345", assessment_id="assessment_67890"
    )
    assert request.user_id == "user_12345"
    assert request.assessment_id == "assessment_67890"


def test_when_user_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="user_id must not be empty"):
        GetQualificationStatusRequest(user_id="", assessment_id="assessment_67890")


def test_when_user_id_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="user_id must be at least 5 characters long"):
        GetQualificationStatusRequest(user_id="usr", assessment_id="assessment_67890")


def test_when_user_id_is_too_long_should_raise_exception():
    long_id = "u" * 101
    with pytest.raises(ValueError, match="user_id must not exceed 100 characters"):
        GetQualificationStatusRequest(user_id=long_id, assessment_id="assessment_67890")


def test_when_user_id_is_exactly_5_characters_should_not_raise():
    request = GetQualificationStatusRequest(
        user_id="usr12", assessment_id="assessment_67890"
    )
    assert request.user_id == "usr12"


def test_when_user_id_is_exactly_100_characters_should_not_raise():
    valid_id = "u" * 100
    request = GetQualificationStatusRequest(
        user_id=valid_id, assessment_id="assessment_67890"
    )
    assert request.user_id == valid_id


def test_when_assessment_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="assessment_id must not be empty"):
        GetQualificationStatusRequest(user_id="user_12345", assessment_id="")


def test_when_assessment_id_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="assessment_id must be at least 5 characters long"
    ):
        GetQualificationStatusRequest(user_id="user_12345", assessment_id="ass")


def test_when_assessment_id_is_too_long_should_raise_exception():
    long_id = "a" * 101
    with pytest.raises(
        ValueError, match="assessment_id must not exceed 100 characters"
    ):
        GetQualificationStatusRequest(user_id="user_12345", assessment_id=long_id)


def test_when_assessment_id_is_exactly_5_characters_should_not_raise():
    request = GetQualificationStatusRequest(user_id="user_12345", assessment_id="ass12")
    assert request.assessment_id == "ass12"


def test_when_assessment_id_is_exactly_100_characters_should_not_raise():
    valid_id = "a" * 100
    request = GetQualificationStatusRequest(
        user_id="user_12345", assessment_id=valid_id
    )
    assert request.assessment_id == valid_id
