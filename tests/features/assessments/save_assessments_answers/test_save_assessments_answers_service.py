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
    AssessmentQuiz,
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


def make_assessment_quiz(user_id: str, questions: list[str]) -> AssessmentQuiz:
    return AssessmentQuiz(
        user_id=user_id, created_at=datetime.now(), questions=questions
    )


@pytest.mark.asyncio
async def test_when_user_and_quiz_are_valid_then_should_save_and_return_success():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)
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
    assessment_repo.get_assessment_quiz.assert_not_called()
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_assessment_quiz_not_found_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(return_value=None)

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "Assessment quiz not found for the given assessment ID."
    assessment_repo.get_assessment.assert_not_called()
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_assessment_already_exists_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(
        return_value=Assessment(
            assessment_id=VALID_ASSESSMENT_ID,
            user_id=VALID_USER_ID,
            created_at=datetime.now(),
            answers=[],
        )
    )

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert (
        response.message
        == "Assessment answers already exist for the given assessment ID."
    )
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_quiz_not_assigned_to_user_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    other_user_id = "other-user-uuid"
    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(other_user_id, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "The assessment quiz does not belong to the user."
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_answered_question_ids_do_not_match_quiz_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request(question_ids=["q-001-uuid-abc", "q-999-invalid"])

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert (
        response.message
        == "Invalid answered question IDs. They must match the questions of the assessment quiz."
    )
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_duplicate_question_ids_in_answers_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, ["q-001", "q-002"])
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = SaveAssessmentsAnswersRequest(
        assessment_id=VALID_ASSESSMENT_ID,
        user_id=VALID_USER_ID,
        answers=[
            AssessmentAnswer(question_id="q-001", answer="A1", takes_time_seconds=10),
            AssessmentAnswer(question_id="q-001", answer="A2", takes_time_seconds=20),
        ],
    )

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert (
        response.message
        == "Invalid answered question IDs. They must match the questions of the assessment quiz."
    )
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_quiz_has_empty_questions_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, [])
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request(question_ids=[])

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert (
        response.message
        == "Invalid answered question IDs. They must match the questions of the assessment quiz."
    )
    assessment_repo.save_assessment_answers.assert_not_called()


@pytest.mark.asyncio
async def test_when_repository_throws_exception_then_should_return_failure():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)
    assessment_repo.save_assessment_answers = AsyncMock(
        side_effect=Exception("Database connection lost")
    )

    service = SaveAssessmentsAnswersService(assessment_repo, user_repo)
    request = make_valid_request()

    response = await service.save_assessment_answers(request)

    assert response.is_success is False
    assert response.message == "An error occurred: Database connection lost"


@pytest.mark.asyncio
async def test_when_success_then_should_call_save_with_correct_assessment_object():
    user_repo = AsyncMock()
    user_repo.get_user_by_id = AsyncMock(return_value=make_user_response())

    assessment_repo = AsyncMock()
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)
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
    assessment_repo.get_assessment_quiz = AsyncMock(
        return_value=make_assessment_quiz(VALID_USER_ID, VALID_QUESTION_IDS)
    )
    assessment_repo.get_assessment = AsyncMock(return_value=None)
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
