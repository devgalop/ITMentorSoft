from unittest.mock import AsyncMock

import pytest

from src.features.assessments.save_assessments_answers.save_assessments_answers_handler import (
    SaveAssessmentsAnswersHandler,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_request import (
    AssessmentAnswer,
    SaveAssessmentsAnswersRequest,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_response import (
    SaveAssessmentsAnswersResponse,
)

VALID_USER_ID = "user-001-uuid-abcdef"
VALID_ASSESSMENT_ID = "assess-001-uuid-abc"
VALID_QUESTION_ID = "q-001-uuid-abc"


def make_valid_request() -> SaveAssessmentsAnswersRequest:
    return SaveAssessmentsAnswersRequest(
        assessment_id=VALID_ASSESSMENT_ID,
        user_id=VALID_USER_ID,
        answers=[
            AssessmentAnswer(
                question_id=VALID_QUESTION_ID,
                answer="Test answer",
                takes_time_seconds=30,
            )
        ],
    )


@pytest.mark.asyncio
async def test_when_service_returns_success_then_handler_should_return_success():
    service_response = SaveAssessmentsAnswersResponse(
        is_success=True, message="Assessment answers saved successfully."
    )

    service = AsyncMock()
    service.save_assessment_answers = AsyncMock(return_value=service_response)

    handler = SaveAssessmentsAnswersHandler(service)
    request = make_valid_request()

    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Assessment answers saved successfully."


@pytest.mark.asyncio
async def test_when_service_returns_failure_then_handler_should_return_same_failure():
    service_response = SaveAssessmentsAnswersResponse(
        is_success=False, message="User not found."
    )

    service = AsyncMock()
    service.save_assessment_answers = AsyncMock(return_value=service_response)

    handler = SaveAssessmentsAnswersHandler(service)
    request = make_valid_request()

    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "User not found."


@pytest.mark.asyncio
async def test_when_handler_is_called_then_should_delegate_to_service():
    service_response = SaveAssessmentsAnswersResponse(is_success=True, message="OK")

    service = AsyncMock()
    service.save_assessment_answers = AsyncMock(return_value=service_response)

    handler = SaveAssessmentsAnswersHandler(service)
    request = make_valid_request()

    await handler.handle(request)

    service.save_assessment_answers.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_handler_is_called_then_should_return_same_response_as_service():
    service_response = SaveAssessmentsAnswersResponse(
        is_success=True, message="Custom message"
    )

    service = AsyncMock()
    service.save_assessment_answers = AsyncMock(return_value=service_response)

    handler = SaveAssessmentsAnswersHandler(service)
    request = make_valid_request()

    response = await handler.handle(request)

    assert response is service_response
