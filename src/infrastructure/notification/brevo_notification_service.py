import json
from typing import List

import aiohttp
from dotenv import load_dotenv
import os

from src.features.shared.notification_service import NotificationConfig, NotificationService

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
BREVO_BASE_API_URL = os.getenv("BREVO_BASE_API_URL", "")

class BrevoNotificationUser:
    """This class represents a user in the Brevo notification system, which can be either a sender or a recipient of a notification.
    """
    def __init__(self, email: str):
        self.email = email

class BrevoNotificationHeader:
    """This class represents the headers for a Brevo notification, including an idempotency key to ensure that the same notification is not sent multiple times.
    """
    def __init__(self, idempotency_key: str):
        self.idempotencyKey = idempotency_key

class BrevoNotificationBody:
    """This class is the representation of Brevo payload to send a notification.
    """
    def __init__(self, 
                 sender: BrevoNotificationUser,
                 to: List[BrevoNotificationUser],
                 subject: str,
                 html_content: str,
                 headers: BrevoNotificationHeader):
        self.sender = sender
        self.to = to
        self.subject = subject
        self.htmlContent = html_content
        self.headers = headers

class BrevoNotificationService(NotificationService):
    
    async def send_notification(self, notification_config: NotificationConfig) -> bool:
        """ Send a notification using Brevo API.

        Args:
            notification_config (NotificationConfig): The configuration for the notification.

        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        headers: dict[str, str] = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        API_URL = f"{BREVO_BASE_API_URL}/smtp/email"
        payload = json.loads(json.dumps(self.to_brevo_payload(notification_config), default=lambda o: o.__dict__))
        
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload, headers=headers) as response:
                data = await response.json()
                if response.status != 201:
                    print(f"Failed to send notification: {data}")
                    return False
        return True
    
    def to_brevo_payload(self, notification_config: NotificationConfig) -> BrevoNotificationBody:
        """Convert a NotificationConfig to a BrevoNotificationBody.

        Args:
            notification_config (NotificationConfig): The configuration for the notification.

        Returns:
            BrevoNotificationBody: The payload for the Brevo API.
        """
        return BrevoNotificationBody(
            sender=BrevoNotificationUser(notification_config.sender),
            to=[BrevoNotificationUser(notification_config.destination)],
            subject=notification_config.subject,
            html_content=notification_config.template or "",
            headers=BrevoNotificationHeader(notification_config.uuid)
        )