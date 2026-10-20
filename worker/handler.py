"""Runs the LiveKit voice agent and wires the stages in order: listening, reasoning, speaking, avatar."""
from worker.stages.avatar.handler import AvatarStage
from worker.stages.listening.handler import ListeningStage
from worker.stages.reasoning.handler import ReasoningStage
from worker.stages.speaking.handler import SpeakingStage


class VoiceAgentWorker:
    def __init__(self):
        self.listening_stage = ListeningStage()
        self.reasoning_stage = ReasoningStage()
        self.speaking_stage = SpeakingStage()
        self.avatar_stage = AvatarStage()

    def run(self):
        """Registers with LiveKit and starts one agent session per conversation."""
        raise NotImplementedError

    async def start_conversation(self, job_context):
        """Builds the agent session from each stage's components, then attaches the avatar."""
        raise NotImplementedError
