from openai import OpenAI

from worker import config


class LanguageModelProvider:
    """Builds the LLM client for the provider set in config. Groq speaks the OpenAI API, so one client type serves both."""

    def __init__(self):
        self.provider_name = config.LLM_PROVIDER
        self.model_name = config.LLM_MODEL

    def build(self):
        if self.provider_name == "groq":
            return OpenAI(api_key=config.GROQ_API_KEY, base_url=config.GROQ_BASE_URL)
        if self.provider_name == "openai":
            return OpenAI(api_key=config.OPENAI_API_KEY)
        raise ValueError(f"Unknown LLM_PROVIDER '{self.provider_name}'. Use 'groq' or 'openai'.")

    def completion_options(self):
        options = {
            "model": self.model_name,
            "temperature": config.LLM_TEMPERATURE,
            "max_completion_tokens": config.LLM_MAX_COMPLETION_TOKENS,
        }
        if config.LLM_REASONING_EFFORT:
            options["reasoning_effort"] = config.LLM_REASONING_EFFORT
        return options
