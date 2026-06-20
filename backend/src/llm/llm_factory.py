from src.llm.base_llm import BaseLLM
from src.llm.openai_client import OpenAIClient


def get_llm() -> BaseLLM:
    """Return the configured LLM client instance (e.g. OpenAIClient routing to Groq)."""
    return OpenAIClient()
