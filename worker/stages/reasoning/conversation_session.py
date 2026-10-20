import time

from worker import config

NO_PASSAGES_TEXT = "(No passage matches this question. Say you don't have that information and suggest contacting the team.)"


class ReplyResult:
    def __init__(self, text, passages, retrieval_seconds, first_token_seconds, total_seconds):
        self.text = text
        self.passages = passages
        self.retrieval_seconds = retrieval_seconds
        self.first_token_seconds = first_token_seconds
        self.total_seconds = total_seconds


class ConversationSession:
    """One customer conversation: keeps the history, retrieves passages per turn and streams the reply."""

    def __init__(self, language_model_client, completion_options, knowledge_lookup, system_prompt_template):
        self.language_model_client = language_model_client
        self.completion_options = completion_options
        self.knowledge_lookup = knowledge_lookup
        self.system_prompt_template = system_prompt_template
        self.history = [{"role": "assistant", "content": config.CONVERSATION_GREETING}]

    def reply(self, user_message, on_text=None):
        started_at = time.perf_counter()
        passages = self.knowledge_lookup.find_relevant_passages(self.build_search_query(user_message))
        retrieval_seconds = time.perf_counter() - started_at

        self.history.append({"role": "user", "content": user_message})
        messages = [{"role": "system", "content": self.build_system_prompt(passages)}]
        messages.extend(self.history)

        stream = self.language_model_client.chat.completions.create(messages=messages, stream=True, **self.completion_options)
        reply_parts = []
        first_token_seconds = None
        for event in stream:
            if not event.choices:
                continue
            delta_text = event.choices[0].delta.content
            if not delta_text:
                continue
            if first_token_seconds is None:
                first_token_seconds = time.perf_counter() - started_at
            reply_parts.append(delta_text)
            if on_text is not None:
                on_text(delta_text)

        reply_text = "".join(reply_parts).strip()
        self.history.append({"role": "assistant", "content": reply_text})
        return ReplyResult(reply_text, passages, retrieval_seconds, first_token_seconds, time.perf_counter() - started_at)

    def build_search_query(self, user_message):
        """Adds the previous customer message so follow-ups like 'and how much is that?' still find the right topic."""
        previous_user_message = ""
        for message in reversed(self.history):
            if message["role"] == "user":
                previous_user_message = message["content"]
                break
        return f"{previous_user_message}\n{user_message}".strip()

    def build_system_prompt(self, passages):
        passage_texts = []
        for passage in passages:
            passage_texts.append(passage.as_prompt_text())
        knowledge_text = "\n\n".join(passage_texts)
        if not knowledge_text:
            knowledge_text = NO_PASSAGES_TEXT
        return self.system_prompt_template.format(
            conversation_language=config.CONVERSATION_LANGUAGE,
            knowledge_passages=knowledge_text,
        )
