from typing import Any
from src.infrastructure.broker.aws.models.aws_sqs_queue import SqsQueue
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnection,
)


class SqsCreatorService:
    def __init__(self, client: SqsConnection):
        self.sqs_client: Any = client.client

    def create_queue(self, queue_name: str) -> SqsQueue:
        existing_queue = self.validate_queue_exists(queue_name)
        if existing_queue:
            return existing_queue
        response = self.sqs_client.create_queue(QueueName=queue_name)
        queue_url: str = response["QueueUrl"]
        return SqsQueue(name=queue_name, queue_url=queue_url)

    def validate_queue_exists(self, queue_name: str) -> SqsQueue | None:
        try:
            queue_url = self.sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
            return SqsQueue(name=queue_name, queue_url=queue_url)
        except self.sqs_client.exceptions.QueueDoesNotExist:
            return None
