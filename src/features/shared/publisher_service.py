from abc import ABC, abstractmethod


class PublishMessageRequest(ABC):
    @abstractmethod
    def get_message(self) -> str:
        """Retrieve the message to be published.

        Returns:
            str: The message to be published.
        """
        pass


class PublishMessageResponse:
    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message


class PublisherService(ABC):
    @abstractmethod
    async def publish(self, request: PublishMessageRequest) -> PublishMessageResponse:
        pass
