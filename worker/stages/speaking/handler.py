from worker import config


class SpeakingStage:
    """Turns the streamed reply text into streamed ElevenLabs speech."""

    def __init__(self):
        self.voice_id = config.ELEVENLABS_VOICE_ID
        self.model_name = config.ELEVENLABS_MODEL

    def build_text_to_speech(self):
        raise NotImplementedError
