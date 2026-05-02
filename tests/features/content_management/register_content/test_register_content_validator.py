from src.features.content_management.register_content.register_content_request import (
    RegisterContentRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = RegisterContentRequest(
        title="Valid Title Here",
        description="This is a valid description with enough characters",
        url="https://example.com/valid",
        category="novice",
        related_topic=["Python"],
    )
    assert request.title == "Valid Title Here"
    assert request.description == "This is a valid description with enough characters"
    assert request.url == "https://example.com/valid"


def test_when_title_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Title must not be empty"):
        RegisterContentRequest(
            title="",
            description="This is a valid description",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_title_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Title must be at least 5 characters long"):
        RegisterContentRequest(
            title="abcd",
            description="This is a valid description",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_title_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Title must not exceed 150 characters"):
        RegisterContentRequest(
            title="a" * 151,
            description="This is a valid description",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_description_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Description must not be empty"):
        RegisterContentRequest(
            title="Valid Title",
            description="",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_description_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Description must be at least 10 characters long"
    ):
        RegisterContentRequest(
            title="Valid Title",
            description="Short",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_description_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Description must not exceed 300 characters"):
        RegisterContentRequest(
            title="Valid Title",
            description="a" * 301,
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_url_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="URL must not be empty"):
        RegisterContentRequest(
            title="Valid Title",
            description="This is a valid description",
            url="",
            category="novice",
            related_topic=[],
        )


def test_when_url_is_invalid_format_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Invalid URL format, must start with https://"
    ):
        RegisterContentRequest(
            title="Valid Title",
            description="This is a valid description",
            url="http://example.com/test",
            category="novice",
            related_topic=[],
        )
