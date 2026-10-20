from worker import config
from worker.livekit.access_tokens import AccessTokenIssuer


class TokenServer:
    """Small HTTP endpoint the web page calls to get a room token; keeps the API secret off the browser."""

    def __init__(self):
        self.token_issuer = AccessTokenIssuer()
        self.host = config.TOKEN_SERVER_HOST
        self.port = config.TOKEN_SERVER_PORT

    def run(self):
        raise NotImplementedError
