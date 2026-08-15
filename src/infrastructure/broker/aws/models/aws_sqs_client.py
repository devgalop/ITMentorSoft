class SqsConnectionRequest:
    def __init__(
        self, endpoint_url: str, access_key: str, secret_key: str, region: str
    ):
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
