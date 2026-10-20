from worker import config
from worker.stages.reasoning.conversation_session import ConversationSession
from worker.stages.reasoning.knowledge_lookup import KnowledgeLookup
from worker.stages.reasoning.language_model_provider import LanguageModelProvider
from worker.stages.reasoning.text_chat_console import TextChatConsole


class ReasoningStage:
    """Produces the agent's streamed reply from the conversation and the knowledge base."""

    def __init__(self):
        self.language_model_provider = LanguageModelProvider()
        self.knowledge_lookup = None

    def rebuild_knowledge_index(self):
        return self.get_knowledge_lookup().rebuild_index()

    def start_conversation(self):
        return ConversationSession(
            self.language_model_provider.build(),
            self.language_model_provider.completion_options(),
            self.get_knowledge_lookup(),
            self.load_system_prompt(),
        )

    def run_text_chat(self):
        TextChatConsole(self.start_conversation()).run()

    def get_knowledge_lookup(self):
        """Loaded on first use: the embedding model takes seconds to load, so it is shared by every conversation."""
        if self.knowledge_lookup is None:
            self.knowledge_lookup = KnowledgeLookup()
        return self.knowledge_lookup

    def load_system_prompt(self):
        return config.SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
