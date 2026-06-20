import os
from typing import Any
from openai import OpenAI
from src.config.settings import settings
from src.llm.base_llm import BaseLLM
from src.logging.logger import logger


class OpenAIClient(BaseLLM):
    """OpenAI-compatible client that routes requests to Groq (or OpenAI)."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model_name: str | None = None,
    ) -> None:
        # Load API key and URL prioritizing Groq configuration, then OpenAI fallback
        self.api_key = (
            api_key
            or settings.groq_api_key
            or settings.openai_api_key
            or os.getenv("GROQ_API_KEY")
            or os.getenv("OPENAI_API_KEY")
        )
        self.base_url = (
            base_url
            or settings.groq_api_url
            or "https://api.groq.com/openai/v1"
        )
        self.model_name = (
            model_name or settings.model_name or "llama-3.3-70b-versatile"
        )

        if not self.api_key:
            logger.warning(
                "No API key configured for OpenAIClient/Groq. LLM calls will fail or use mock."
            )
            self.client = None
        else:
            logger.info(
                "Initializing OpenAIClient targeting base_url={}", self.base_url
            )
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate response text from chat messages."""
        if not self.client:
            raise RuntimeError(
                "OpenAIClient is not initialized with an API key. Please check your config."
            )

        model = kwargs.pop("model", self.model_name)
        logger.info("Sending chat completion request to model={}", model)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs,
            )
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("Received empty content from LLM.")
            return content
        except Exception as exc:
            logger.exception("LLM generation request failed.")
            raise RuntimeError("LLM completion failed.") from exc
