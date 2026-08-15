from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnection,
)


class SqsPublisherService:
    def __init__(self, sqs_client: SqsConnection):
        self.sqs_client = sqs_client

    async def publish(self, queue_url: str, message: str):
        """Publish a message to the specified SQS queue.

        Args:
            queue_url (str): The URL of the SQS queue.
            message (str): The message to be published.

        Returns:
            dict: The response from the SQS service.
        """
        response = await self.sqs_client.client.send_message(
            QueueUrl=queue_url, MessageBody=message
        )
        return response
