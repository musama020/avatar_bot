from worker import config


class FlashHeadAvatarClient:
    """Agent side: forwards TTS audio to the avatar server and tells it to clear when the user interrupts."""

    def __init__(self):
        self.server_address = f"ws://{config.AVATAR_SERVER_HOST}:{config.AVATAR_SERVER_PORT}"

    async def start(self, agent_session, room):
        raise NotImplementedError
