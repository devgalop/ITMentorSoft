from src.features.assessments.get_question_categories.get_question_categories_request import (
    GetQuestionCategoriesRequest,
)
import pytest


def test_when_version_is_valid_then_exception_is_not_raised():
    for version in [1, 5, 10]:
        request = GetQuestionCategoriesRequest(version=version)
        assert request.version == version


def test_when_version_is_zero_then_exception_is_raised():
    with pytest.raises(ValueError, match="version must be greater than 0"):
        GetQuestionCategoriesRequest(version=0)


def test_when_version_is_negative_then_exception_is_raised():
    with pytest.raises(ValueError, match="version must be greater than 0"):
        GetQuestionCategoriesRequest(version=-1)


def test_when_version_exceeds_maximum_then_exception_is_raised():
    with pytest.raises(ValueError, match="version must be less than or equal to 10"):
        GetQuestionCategoriesRequest(version=11)


def test_when_version_is_far_above_maximum_then_exception_is_raised():
    with pytest.raises(ValueError, match="version must be less than or equal to 10"):
        GetQuestionCategoriesRequest(version=100)
