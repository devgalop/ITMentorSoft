from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.features.shared.notification_service import NotificationConfig
from src.infrastructure.notification.brevo_notification_service import (
    BrevoNotificationService,
)

# ── Group A: to_brevo_payload (synchronous) ──────────────────────────────────


def test_when_config_has_sender_then_payload_sender_email_matches():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Test Subject")

    payload = service.to_brevo_payload(config)

    assert payload.sender.email == "sender@test.com"


def test_when_config_has_destination_then_payload_to_contains_email():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Test Subject")

    payload = service.to_brevo_payload(config)

    assert payload.to[0].email == "dest@test.com"


def test_when_config_has_subject_then_payload_subject_matches():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Test Subject")

    payload = service.to_brevo_payload(config)

    assert payload.subject == "Test Subject"


def test_when_template_is_none_then_payload_html_content_is_empty_string():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Test Subject")
    config.template = None

    payload = service.to_brevo_payload(config)

    assert payload.htmlContent == ""


def test_when_template_is_provided_then_payload_html_content_matches():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Test Subject")
    config.template = "<h1>Hello</h1>"

    payload = service.to_brevo_payload(config)

    assert payload.htmlContent == "<h1>Hello</h1>"


def test_when_config_has_uuid_then_payload_header_idempotency_key_matches():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Test Subject")

    payload = service.to_brevo_payload(config)

    assert payload.headers.idempotencyKey == config.uuid


# ── Group B: send_notification (async, mock aiohttp) ─────────────────────────


@pytest.mark.asyncio
async def test_when_api_responds_201_then_send_notification_returns_true():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Subject")
    config.template = "<p>Hello</p>"

    mock_response = AsyncMock()
    mock_response.status = 201
    mock_response.json = AsyncMock(return_value={"messageId": "test-id"})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch(
        "src.infrastructure.notification.brevo_notification_service.aiohttp.ClientSession",
        return_value=mock_session,
    ):
        result = await service.send_notification(config)

    assert result is True


@pytest.mark.asyncio
async def test_when_api_responds_400_then_send_notification_returns_false():
    service = BrevoNotificationService()
    config = NotificationConfig("sender@test.com", "dest@test.com", "Subject")
    config.template = "<p>Hello</p>"

    mock_response = AsyncMock()
    mock_response.status = 400
    mock_response.json = AsyncMock(
        return_value={"message": "Bad request", "code": "invalid_parameter"}
    )
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch(
        "src.infrastructure.notification.brevo_notification_service.aiohttp.ClientSession",
        return_value=mock_session,
    ):
        result = await service.send_notification(config)

    assert result is False
