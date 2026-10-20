from worker.stages.avatar.avatar_client import FlashHeadAvatarClient
from worker.stages.avatar.avatar_server import FlashHeadAvatarServer


class AvatarStage:
    """Shows the talking face. The avatar, not the agent, sends the audio to the user, so lips and voice stay in sync."""

    async def attach_to_session(self, agent_session, room):
        await FlashHeadAvatarClient().start(agent_session, room)

    def start_avatar_server(self):
        FlashHeadAvatarServer().run()
