from worker.stages.listening.speech_client import NemotronSpeechToText
from worker.stages.listening.speech_server import NemotronSpeechServer


class ListeningStage:
    """Turns the user's audio into text and decides when they have finished speaking."""

    def build_voice_activity_detector(self):
        raise NotImplementedError

    def build_speech_to_text(self):
        return NemotronSpeechToText()

    def build_turn_detector(self):
        raise NotImplementedError

    def start_speech_server(self):
        NemotronSpeechServer().run()
