from worker import config


class AccessTokenIssuer:
    """Signs LiveKit room tokens; shared by the token server and the avatar, which joins rooms itself."""

    def __init__(self):
        self.api_key = config.LIVEKIT_API_KEY
        self.api_secret = config.LIVEKIT_API_SECRET

    def issue_token(self, room_name, participant_identity):
        raise NotImplementedError
