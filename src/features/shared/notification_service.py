from abc import ABC, abstractmethod
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationConfig:
    """This class contains the main configuration to send notifications, such as sender, destination, subject, template and attachments."""

    def __init__(self, sender: str, destination: str, subject: str):
        self.uuid: str = uuid.uuid4().hex
        self.sender = sender
        self.destination = destination
        self.subject = subject
        self.template: str | None = None
        self.attachments: list[str] = []


class NotificationConfigBuilder:
    """Class to build notification configuration with a fluent interface"""

    def __init__(self, destination: str, subject: str):
        default_sender = os.getenv("EMAIL_DEFAULT_SENDER", "")
        self.config = NotificationConfig(default_sender, destination, subject)

    def set_template(self, template: str) -> "NotificationConfigBuilder":
        """Add a template body for the notification.

        Args:
            template (str): The template body for the notification.

        Returns:
            NotificationConfigBuilder: The builder instance.
        """
        self.config.template = template
        return self

    def add_attachment(self, attachment: str) -> "NotificationConfigBuilder":
        """Add an attachment to the notification.

        Args:
            attachment (str): The file path of the attachment.

        Returns:
            NotificationConfigBuilder: The builder instance.
        """
        self.config.attachments.append(attachment)
        return self

    def build(self) -> NotificationConfig:
        return self.config


class NotificationService(ABC):
    @abstractmethod
    async def send_notification(self, notification_config: NotificationConfig) -> bool:
        """Send a notification to a recipient.

        Args:
            notification_config (NotificationConfig): The configuration for the notification.

        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        pass
