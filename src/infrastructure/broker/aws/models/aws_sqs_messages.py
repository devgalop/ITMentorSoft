from abc import ABC, abstractmethod


class SqsMessage(ABC):

    @abstractmethod
    def serialize(self) -> str:
        """Generate string representation of the message.

        Returns:
            str: The serialized string representation of the message.
        """
        pass


class SqsMessageReceived:
    def __init__(
        self, message_id: str, body: str, receipt_handle: str, retry_count: int = 0
    ):
        self.message_id = message_id
        self.body = body
        self.receipt_handle = receipt_handle
        self.retry_count = retry_count
