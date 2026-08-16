from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_qualification_status.get_qualification_status_handler import (
    GetQualificationStatusHandler,
)
from src.features.assessments.get_qualification_status.get_qualification_status_request import (
    GetQualificationStatusRequest,
)


@pytest.mark.asyncio
async def test_when_qualification_is_completed_should_return_true():
    assessment_repository = AsyncMock()
    assessment_repository.is_qualification_completed = AsyncMock(return_value=True)

    handler = GetQualificationStatusHandler(assessment_repository)
    request = GetQualificationStatusRequest(
        user_id="user_12345", assessment_id="assessment_67890"
    )
    response = await handler.handle(request)

    assert response.is_already_qualified is True
    assessment_repository.is_qualification_completed.assert_called_once_with(
        "user_12345", "assessment_67890"
    )


@pytest.mark.asyncio
async def test_when_qualification_is_not_completed_should_return_false():
    assessment_repository = AsyncMock()
    assessment_repository.is_qualification_completed = AsyncMock(return_value=False)

    handler = GetQualificationStatusHandler(assessment_repository)
    request = GetQualificationStatusRequest(
        user_id="user_12345", assessment_id="assessment_67890"
    )
    response = await handler.handle(request)

    assert response.is_already_qualified is False
    assessment_repository.is_qualification_completed.assert_called_once_with(
        "user_12345", "assessment_67890"
    )
