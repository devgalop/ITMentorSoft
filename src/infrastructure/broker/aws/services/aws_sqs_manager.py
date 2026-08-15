import os
from dotenv import load_dotenv
from src.infrastructure.broker.aws.models.aws_sqs_client import SqsConnectionRequest
from src.infrastructure.broker.aws.models.aws_sqs_consumer_config import (
    SqsConsumerConfig,
)
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnectionFactoryService,
)
from src.infrastructure.broker.aws.services.aws_sqs_consumer_qualification import (
    SqsConsumerQualification,
)
from src.infrastructure.broker.aws.services.aws_sqs_creator_service import (
    SqsCreatorService,
)

load_dotenv()

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "test")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
REGION = os.getenv("AWS_REGION", "us-east-1")
BASE_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

AWS_SQS_QUALIFICATION_QUEUE_URL = os.getenv(
    "AWS_SQS_QUALIFICATION_QUEUE_URL",
    "http://localhost:4566/000000000000/mq-itmentorsoft-qualify-001",
)
AWS_SQS_CLASSIFICATION_QUEUE_URL = os.getenv(
    "AWS_SQS_CLASSIFICATION_QUEUE_URL",
    "http://localhost:4566/000000000000/mq-itmentorsoft-classify-001",
)


class SqsManagerService:

    @staticmethod
    def create_queues():
        sqs_connection_factory = SqsConnectionFactoryService(
            connection_request=SqsConnectionRequest(
                endpoint_url=BASE_URL,
                access_key=ACCESS_KEY,
                secret_key=SECRET_KEY,
                region=REGION,
            )
        )
        sqs_connection = sqs_connection_factory.create_connection()
        sqs_creator_service = SqsCreatorService(sqs_connection)
        sqs_creator_service.create_queue("mq-itmentorsoft-qualify-001")
        sqs_creator_service.create_queue("mq-itmentorsoft-classify-001")

    @staticmethod
    def start_consumer_services():
        # Initialize the SQS connection and configuration
        sqs_config = SqsConsumerConfig(
            queue_url=AWS_SQS_QUALIFICATION_QUEUE_URL,
            max_messages=10,
            wait_time_seconds=20,
            is_enabled=True,
        )
        sqs_connection_factory = SqsConnectionFactoryService(
            connection_request=SqsConnectionRequest(
                endpoint_url=BASE_URL,
                access_key=ACCESS_KEY,
                secret_key=SECRET_KEY,
                region=REGION,
            )
        )

        # Create an instance of the SqsConsumerQualification service
        sqs_connection = sqs_connection_factory.create_connection()
        sqs_consumer_service = SqsConsumerQualification(sqs_config, sqs_connection)

        # Start the consumer service
        sqs_consumer_service.start_consumer()
