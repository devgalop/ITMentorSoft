from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.features.reports.get_student_summary.get_student_summary_endpoint import (
    router as student_summary_router,
)
from src.features.reports.get_student_summary.get_student_summary_response import (
    GetStudentSummaryResponse,
    SummaryResponse,
)
from src.features.reports.get_student_summary.get_student_summary_handler import (
    GetStudentSummaryHandler,
)
from src.features.user_management.shared.token_generator import TokenData

STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def make_test_app(handler: GetStudentSummaryHandler) -> FastAPI:
    """Create a test app with the student summary router and overridden dependencies."""
    from src.features.reports.shared.dependencies import get_get_student_summary_handler
    from src.features.user_management.shared.get_current_user import get_current_user

    app = FastAPI()
    app.include_router(student_summary_router)

    def override_handler():
        return handler

    def override_auth():
        return TokenData(user_name="testuser", role="admin")

    app.dependency_overrides[get_get_student_summary_handler] = override_handler
    app.dependency_overrides[get_current_user] = override_auth

    return app


def make_success_response() -> GetStudentSummaryResponse:
    return GetStudentSummaryResponse(
        is_success=True,
        message="Student summary retrieved successfully",
        summary=SummaryResponse(
            student_id=STUDENT_ID,
            name="Test Student",
            knowledge_classification="Advanced",
            profile=[],
            feedback="Good progress",
        ),
    )


def make_handler(return_value: GetStudentSummaryResponse) -> GetStudentSummaryHandler:
    handler = GetStudentSummaryHandler(AsyncMock())
    handler.handle = AsyncMock(return_value=return_value)
    return handler


def test_when_valid_request_then_return_200():
    handler = make_handler(make_success_response())
    client = TestClient(make_test_app(handler))

    response = client.get(f"/student_summary?id={STUDENT_ID}")

    assert response.status_code == 200
    data = response.json()
    assert data["is_success"] is True
    assert data["message"] == "Student summary retrieved successfully"
    assert data["summary"]["student_id"] == STUDENT_ID
    assert data["summary"]["name"] == "Test Student"


def test_when_student_not_found_then_return_404():
    handler = make_handler(
        GetStudentSummaryResponse(
            is_success=False,
            message="Student not found",
            summary=None,
        )
    )
    client = TestClient(make_test_app(handler))

    response = client.get(f"/student_summary?id={STUDENT_ID}")

    assert response.status_code == 404
    data = response.json()
    assert "Student not found" in data["detail"]


def test_when_empty_id_then_return_400():
    handler = make_handler(make_success_response())
    client = TestClient(make_test_app(handler))

    response = client.get("/student_summary?id=")

    assert response.status_code == 400
    data = response.json()
    assert "User ID is required" in data["detail"]


def test_when_missing_id_param_then_return_422():
    handler = make_handler(make_success_response())
    client = TestClient(make_test_app(handler))

    response = client.get("/student_summary")

    assert response.status_code == 422
