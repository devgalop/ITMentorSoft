from src.infrastructure.broker.aws.models.aws_sqs_messages import SqsMessageReceived
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnection,
)
from src.infrastructure.broker.aws.services.aws_sqs_consumer_service import (
    SqsConsumerService,
)
from src.infrastructure.broker.aws.models.aws_sqs_consumer_config import (
    SqsConsumerConfig,
)


class SqsConsumerQualification(SqsConsumerService):
    def __init__(self, sqs_config: SqsConsumerConfig, sqs_client: SqsConnection):
        super().__init__(sqs_client, sqs_config)

    async def process_message(self, message: SqsMessageReceived):
        # Implement the logic to process the message here
        print(f"Processing message: {message.message_id} with body: {message.body}")
        # After processing, you might want to delete the message from the queue
        await self.sqs_client.client.delete_message(
            queue_url=self.sqs_config.queue_url, receipt_handle=message.receipt_handle
        )
