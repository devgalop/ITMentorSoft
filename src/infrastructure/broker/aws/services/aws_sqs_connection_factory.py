from typing import Any
import boto3
from src.infrastructure.broker.aws.models.aws_sqs_client import SqsConnectionRequest


class SqsConnection:
    def __init__(self, client: Any):
        self.client = client


class SqsConnectionFactoryService:
    def __init__(self, connection_request: SqsConnectionRequest):
        self.connection_request = connection_request

    def create_connection(self) -> SqsConnection:
        client: Any = boto3.client(
            "sqs",
            endpoint_url=self.connection_request.endpoint_url,
            aws_access_key_id=self.connection_request.access_key,
            aws_secret_access_key=self.connection_request.secret_key,
            region_name=self.connection_request.region,
        )
        return SqsConnection(client=client)
