from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """Abstract Base Class for LLM Clients."""

    @abstractmethod
    def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate response text from a list of chat messages."""
        pass
