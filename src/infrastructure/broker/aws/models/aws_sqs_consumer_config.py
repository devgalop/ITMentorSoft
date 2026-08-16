class SqsConsumerConfig:
    def __init__(
        self,
        queue_url: str,
        max_messages: int = 10,
        wait_time_seconds: int = 20,
        is_enabled: bool = False,
    ):
        self.queue_url = queue_url
        self.max_messages = max_messages
        self.wait_time_seconds = wait_time_seconds
        self.is_enabled = is_enabled
