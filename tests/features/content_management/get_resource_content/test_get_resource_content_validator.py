from src.features.content_management.get_resource_content.get_resource_content_request import (
    GetResourceRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetResourceRequest(content_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
    assert request.content_id == "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def test_when_content_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Content ID must not be empty"):
        GetResourceRequest(content_id="")


def test_when_content_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Content ID must be at least 10 characters long"
    ):
        GetResourceRequest(content_id="abc123")


def test_when_content_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Content ID must not exceed 100 characters"):
        GetResourceRequest(content_id="a" * 101)
