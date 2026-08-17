import pytest

from src.features.content_management.update_resource_status.update_resource_status_request import (
    UpdateResourceStatusRequest,
)


def test_when_content_id_and_status_are_valid_should_not_raise():
    request = UpdateResourceStatusRequest(content_id="resource_123", status=True)
    assert request.content_id == "resource_123"
    assert request.status is True


def test_when_content_id_is_empty_should_raise():
    with pytest.raises(ValueError, match="content_id must not be empty"):
        UpdateResourceStatusRequest(content_id="", status=True)


def test_when_content_id_is_too_short_should_raise():
    with pytest.raises(
        ValueError, match="content_id must be at least 5 characters long"
    ):
        UpdateResourceStatusRequest(content_id="abc", status=True)


def test_when_content_id_is_exactly_5_characters_should_not_raise():
    request = UpdateResourceStatusRequest(content_id="abcde", status=False)
    assert request.content_id == "abcde"


def test_when_content_id_is_at_maximum_length_should_not_raise():
    max_content_id = "a" * 100
    request = UpdateResourceStatusRequest(content_id=max_content_id, status=True)
    assert request.content_id == max_content_id


def test_when_content_id_exceeds_100_characters_should_raise():
    long_content_id = "a" * 101
    with pytest.raises(ValueError, match="content_id must not exceed 100 characters"):
        UpdateResourceStatusRequest(content_id=long_content_id, status=True)


def test_when_status_is_true_should_accept():
    request = UpdateResourceStatusRequest(content_id="resource_123", status=True)
    assert request.status is True


def test_when_status_is_false_should_accept():
    request = UpdateResourceStatusRequest(content_id="resource_123", status=False)
    assert request.status is False
