"""Single entry point. Usage: python main.py <process>, where process is one of PROCESS_NAMES."""
import argparse

PROCESS_NAMES = ["agent", "speech", "avatar", "token", "index-knowledge", "chat", "reasoning-test", "avatar-latency-test"]


class ProcessLauncher:
    """Starts one named process. Imports stay inside each branch so the agent never loads GPU libraries."""

    def launch(self, process_name):
        if process_name == "agent":
            from worker.handler import VoiceAgentWorker
            VoiceAgentWorker().run()
        elif process_name == "speech":
            from worker.stages.listening.handler import ListeningStage
            ListeningStage().start_speech_server()
        elif process_name == "avatar":
            from worker.stages.avatar.handler import AvatarStage
            AvatarStage().start_avatar_server()
        elif process_name == "token":
            from worker.livekit.token_server import TokenServer
            TokenServer().run()
        elif process_name == "index-knowledge":
            from worker.stages.reasoning.handler import ReasoningStage
            chunks = ReasoningStage().rebuild_knowledge_index()
            print(f"Indexed {len(chunks)} knowledge chunks")
        elif process_name == "chat":
            from worker.stages.reasoning.handler import ReasoningStage
            ReasoningStage().run_text_chat()
        elif process_name == "reasoning-test":
            from evaluation.reasoning_test import ReasoningTest
            ReasoningTest().run()
        elif process_name == "avatar-latency-test":
            from evaluation.flashhead_latency import FlashHeadLatencyTest
            FlashHeadLatencyTest().run()


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description="Avatar chatbot processes")
    argument_parser.add_argument("process", choices=PROCESS_NAMES)
    arguments = argument_parser.parse_args()
    ProcessLauncher().launch(arguments.process)
