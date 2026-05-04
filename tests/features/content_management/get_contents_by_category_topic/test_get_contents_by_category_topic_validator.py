import pytest
from pydantic import ValidationError

from src.features.content_management.get_contents_by_category_topic.get_contents_by_category_topic_request import (
    GetContentsByCategoryTopicRequest,
    GetContentsByCategoryTopicPaginationRequest,
)


def test_when_category_and_topic_are_valid_then_exception_is_not_raised():
    req = GetContentsByCategoryTopicRequest(category="novice", topic="Python")
    assert req.category == "novice"
    assert req.topic == "Python"


def test_when_category_has_whitespace_then_strips_it():
    req = GetContentsByCategoryTopicRequest(category="  novice  ", topic="Python")
    assert req.category == "novice"


def test_when_topic_has_whitespace_then_strips_it():
    req = GetContentsByCategoryTopicRequest(category="novice", topic="  Python  ")
    assert req.topic == "Python"


def test_when_category_is_too_short_then_raises_validation_error():
    with pytest.raises(ValidationError, match="at least 3 characters"):
        GetContentsByCategoryTopicRequest(category="no", topic="Python")


def test_when_topic_is_too_short_then_raises_validation_error():
    with pytest.raises(ValidationError, match="at least 3 characters"):
        GetContentsByCategoryTopicRequest(category="novice", topic="Py")


def test_when_category_is_too_long_then_raises_validation_error():
    with pytest.raises(ValidationError, match="exceed 100 characters"):
        GetContentsByCategoryTopicRequest(category="a" * 101, topic="Python")


def test_when_topic_is_too_long_then_raises_validation_error():
    with pytest.raises(ValidationError, match="exceed 100 characters"):
        GetContentsByCategoryTopicRequest(category="novice", topic="a" * 101)


def test_when_category_is_empty_whitespace_then_raises_validation_error():
    with pytest.raises(ValidationError, match="must not be empty"):
        GetContentsByCategoryTopicRequest(category="   ", topic="Python")


def test_when_topic_is_empty_whitespace_then_raises_validation_error():
    with pytest.raises(ValidationError, match="must not be empty"):
        GetContentsByCategoryTopicRequest(category="novice", topic="   ")


def test_when_pagination_uses_defaults_then_page_is_zero_and_page_size_is_ten():
    req = GetContentsByCategoryTopicPaginationRequest(category="novice", topic="Python")
    assert req.page == 0
    assert req.page_size == 10


def test_when_page_is_negative_then_raises_validation_error():
    with pytest.raises(ValidationError, match="at least 0"):
        GetContentsByCategoryTopicPaginationRequest(
            category="novice", topic="Python", page=-1
        )


def test_when_page_size_is_zero_then_raises_validation_error():
    with pytest.raises(ValidationError, match="between 1 and 100"):
        GetContentsByCategoryTopicPaginationRequest(
            category="novice", topic="Python", page_size=0
        )


def test_when_page_size_exceeds_100_then_raises_validation_error():
    with pytest.raises(ValidationError, match="between 1 and 100"):
        GetContentsByCategoryTopicPaginationRequest(
            category="novice", topic="Python", page_size=101
        )


def test_when_pagination_has_valid_custom_values_then_exception_is_not_raised():
    req = GetContentsByCategoryTopicPaginationRequest(
        category="novice", topic="Python", page=2, page_size=50
    )
    assert req.page == 2
    assert req.page_size == 50
