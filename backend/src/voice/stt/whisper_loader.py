from functools import lru_cache
from typing import Any

try:
    import whisper
except ImportError:
    class DummyWhisper:
        @staticmethod
        def load_model(model_name: str) -> Any:
            raise ImportError("The 'whisper' module is not installed in this environment.")
    whisper = DummyWhisper()

from src.config.settings import settings
from src.logging.logger import logger


@lru_cache(maxsize=1)
def _load_model(model_name: str) -> Any:
    logger.info("Whisper model load requested: {}", model_name)
    model = whisper.load_model(model_name)
    logger.info("Whisper model loaded: {}", model_name)
    return model


def load_whisper() -> Any:
    """Load and cache the configured Whisper model."""

    return _load_model(settings.whisper_model or "base")
