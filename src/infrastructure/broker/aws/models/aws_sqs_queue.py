class SqsQueue:
    def __init__(self, name: str, queue_url: str):
        self.name = name
        self.queue_url = queue_url
