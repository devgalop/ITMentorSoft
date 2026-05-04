import pytest

from src.features.content_management.rate_content.rate_content_request import (
    RateContentRequest,
)


def test_when_request_is_valid_then_exception_is_not_raised():
    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
        comment="Great content!",
    )
    assert request.content_id == "valid_content_id_123"
    assert request.user_id == "valid_user_id_456"
    assert request.rating == 4
    assert request.comment == "Great content!"


def test_when_content_id_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Content ID must not be empty"):
        RateContentRequest(
            content_id="",
            user_id="valid_user_id_456",
            rating=4,
        )


def test_when_content_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Content ID must be at least 10 characters long"
    ):
        RateContentRequest(
            content_id="short",
            user_id="valid_user_id_456",
            rating=4,
        )


def test_when_content_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Content ID must not exceed 100 characters"):
        RateContentRequest(
            content_id="a" * 101,
            user_id="valid_user_id_456",
            rating=4,
        )


def test_when_user_id_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="User ID must not be empty"):
        RateContentRequest(
            content_id="valid_content_id_123",
            user_id="",
            rating=4,
        )


def test_when_user_id_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="User ID must be at least 10 characters long"):
        RateContentRequest(
            content_id="valid_content_id_123",
            user_id="short",
            rating=4,
        )


def test_when_user_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="User ID must not exceed 100 characters"):
        RateContentRequest(
            content_id="valid_content_id_123",
            user_id="a" * 101,
            rating=4,
        )


def test_when_rating_is_below_range_then_exception_is_raised():
    with pytest.raises(ValueError, match="Rating must be between 0 and 5"):
        RateContentRequest(
            content_id="valid_content_id_123",
            user_id="valid_user_id_456",
            rating=-1,
        )


def test_when_rating_is_above_range_then_exception_is_raised():
    with pytest.raises(ValueError, match="Rating must be between 0 and 5"):
        RateContentRequest(
            content_id="valid_content_id_123",
            user_id="valid_user_id_456",
            rating=6,
        )


def test_when_rating_is_at_valid_boundaries_then_exception_is_not_raised():
    request_min = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=0,
    )
    assert request_min.rating == 0

    request_max = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=5,
    )
    assert request_max.rating == 5


def test_when_comment_is_not_provided_then_default_is_none():
    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
    )
    assert request.comment is None


def test_when_rating_is_zero_then_exception_is_not_raised():
    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=0,
    )
    assert request.rating == 0


def test_when_rating_is_five_then_exception_is_not_raised():
    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=5,
    )
    assert request.rating == 5
