from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.features.assessments.save_assessments_answers.save_assessments_answers_request import (
    AssessmentAnswer,
    SaveAssessmentsAnswersRequest,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_service import (
    SaveAssessmentsAnswersService,
)
from src.features.assessments.shared.assessment import (
    Assessment,
)
from src.features.user_management.shared.user import UserResponse, UserStatus, UserRole

VALID_USER_ID = "user-001-uuid-abcdef"
VALID_ASSESSMENT_ID = "assess-001-uuid-abc"
VALID_QUESTION_IDS = ["q-001-uuid-abc", "q-002-uuid-def", "q-003-uuid-ghi"]


def make_user_response() -> UserResponse:
    return UserResponse(
        id=VALID_USER_ID,
        username="testuser",
        email="test@example.com",
        status=UserStatus.ACTIVE,
        role=UserRole.STUDENT,
    )


def make_valid_request(
    question_ids: list[str] | None = None,
) -> SaveAssessmentsAnswersRequest:
    qids = question_ids or VALID_QUESTION_IDS
    answers = [
        AssessmentAnswer(
            question_id=qid, answer=f"Answer for {qid}", takes_time_seconds=30
        )
        for qid in qids
    ]
    return SaveAssessmentsAnswersRequest(
        assessment_id=VALID_ASSESSMENT_ID,
        user_id=VALID_USER_ID,
        answers=answers,
    )


@pytest.mark.asyncio
async def test_when_user_and_questions_are_valid_then_should_save_and_return_success():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=VALID_QUESTION_IDS)
    assessment_repo.save_assessment_answers = AsyncMock()

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is True
    assert response.message == "Assessment answers saved successfully."
    assessment_repo.save_assessment_answers.assert_called_once()


@pytest.mark.asyncio
async def test_when_user_not_found_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=None)

    assessment_repo = AsyncMock()

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "User not found."
    assessment_repo.get_questions_per_quiz.assert_not_called()
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_assessment_has_no_questions_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=[])

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "Invalid assessment ID or answers."
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_more_answers_than_questions_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=["q-001"])

    extra_answers = [
        AssessmentAnswer(question_id="q-001", answer="A1", takes_time_seconds=10),
        AssessmentAnswer(question_id="q-002", answer="A2", takes_time_seconds=20),
    ]
    request = SaveAssessmentsAnswersRequest(
        assessment_id=VALID_ASSESSMENT_ID,
        user_id=VALID_USER_ID,
        answers=extra_answers,
    )

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "Invalid assessment ID or answers."
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_fewer_answers_than_questions_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(
        return_value=["q-001", "q-002", "q-003"]
    )

    request = SaveAssessmentsAnswersRequest(
        assessment_id=VALID_ASSESSMENT_ID,
        user_id=VALID_USER_ID,
        answers=[
            AssessmentAnswer(question_id="q-001", answer="A1", takes_time_seconds=10),
        ],
    )

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "Invalid assessment ID or answers."
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_question_id_not_in_assessment_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=["q-001", "q-002"])

    request = SaveAssessmentsAnswersRequest(
        assessment_id=VALID_ASSESSMENT_ID,
        user_id=VALID_USER_ID,
        answers=[
            AssessmentAnswer(question_id="q-001", answer="A1", takes_time_seconds=10),
            AssessmentAnswer(
                question_id="q-999-invalid", answer="A2", takes_time_seconds=20
            ),
        ],
    )

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert "Invalid question ID: q-999-invalid." == response.message
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_repository_throws_exception_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=VALID_QUESTION_IDS)
    assessment_repo.save_assessment_answers = AsyncMock(
        side_effect=Exception("Database connection lost")
    )

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert "An error occurred: Database connection lost" == response.message


@pytest.mark.asyncio
async def test_when_success_then_should_call_save_with_correct_assessment_object():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=VALID_QUESTION_IDS)
    assessment_repo.save_assessment_answers = AsyncMock()

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    await service.save_assessment_answers(request)

    assessment_repo.save_assessment_answers.assert_called_once()
    saved_assessment: Assessment = assessment_repo.save_assessment_answers.call_args[0][
        0
    ]

    assert isinstance(saved_assessment, Assessment)
    assert saved_assessment.user_id == VALID_USER_ID
    assert saved_assessment.assessment_id == VALID_ASSESSMENT_ID
    assert len(saved_assessment.answers) == len(VALID_QUESTION_IDS)
    assert isinstance(saved_assessment.created_at, datetime)


@pytest.mark.asyncio
async def test_when_success_then_assessment_answers_should_match_request():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_questions_per_quiz = AsyncMock(return_value=VALID_QUESTION_IDS)
    assessment_repo.save_assessment_answers = AsyncMock()

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    await service.save_assessment_answers(request)

    saved_assessment: Assessment = assessment_repo.save_assessment_answers.call_args[0][
        0
    ]
    saved_answer_map = {a.question_id: a for a in saved_assessment.answers}

    for req_answer in request.answers:
        assert req_answer.question_id in saved_answer_map
        domain_answer = saved_answer_map[req_answer.question_id]
        assert domain_answer.answer == req_answer.answer
        assert domain_answer.time_taken_seconds == req_answer.takes_time_seconds
