import pytest
from pydantic import ValidationError

from src.features.content_management.get_contents_by_category.get_contents_by_category_request import (
    GetContentsByCategoryRequest,
    GetContentsByCategoryPaginationRequest,
)


def test_when_category_is_valid_then_exception_is_not_raised():
    req = GetContentsByCategoryRequest(category="Python")
    assert req.category == "Python"


def test_when_category_has_whitespace_then_strips_it():
    req = GetContentsByCategoryRequest(category="  Python  ")
    assert req.category == "Python"


def test_when_category_is_too_short_then_raises_validation_error():
    with pytest.raises(ValidationError, match="at least 3 characters"):
        GetContentsByCategoryRequest(category="Py")


def test_when_category_is_too_long_then_raises_validation_error():
    with pytest.raises(ValidationError, match="exceed 100 characters"):
        GetContentsByCategoryRequest(category="a" * 101)


def test_when_category_is_empty_whitespace_then_raises_validation_error():
    with pytest.raises(ValidationError, match="must not be empty"):
        GetContentsByCategoryRequest(category="   ")


def test_when_pagination_uses_defaults_then_page_is_zero_and_page_size_is_ten():
    req = GetContentsByCategoryPaginationRequest(category="Python")
    assert req.page == 0
    assert req.page_size == 10


def test_when_page_is_negative_then_raises_validation_error():
    with pytest.raises(ValidationError, match="at least 0"):
        GetContentsByCategoryPaginationRequest(category="Python", page=-1)


def test_when_page_size_is_zero_then_raises_validation_error():
    with pytest.raises(ValidationError, match="between 1 and 100"):
        GetContentsByCategoryPaginationRequest(category="Python", page_size=0)


def test_when_page_size_exceeds_100_then_raises_validation_error():
    with pytest.raises(ValidationError, match="between 1 and 100"):
        GetContentsByCategoryPaginationRequest(category="Python", page_size=101)


def test_when_pagination_has_valid_custom_values_then_exception_is_not_raised():
    req = GetContentsByCategoryPaginationRequest(
        category="Python", page=2, page_size=50
    )
    assert req.page == 2
    assert req.page_size == 50
