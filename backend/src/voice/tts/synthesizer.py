import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

from gtts import gTTS

from src.config.settings import settings
from src.logging.logger import logger


class TextToSpeechError(RuntimeError):
    """Raised when text-to-speech generation fails."""


class TextToSpeechProvider(ABC):
    """Provider interface for swappable TTS engines."""

    @abstractmethod
    def synthesize_to_file(self, text: str, output_path: Path) -> Path:
        """Generate speech audio for text and write it to output_path."""


class GTTSProvider(TextToSpeechProvider):
    def __init__(self, language: str = "en") -> None:
        self.language = language

    def synthesize_to_file(self, text: str, output_path: Path) -> Path:
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save(str(output_path))
        return output_path


def _validate_text(text: str) -> str:
    if text is None:
        raise ValueError("Text cannot be None.")

    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Empty text cannot be synthesized.")

    return cleaned


def synthesize(text: str) -> str:
    """Convert text into speech and return the generated audio path."""

    cleaned_text = _validate_text(text)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        output_path = Path(temp_file.name)

    logger.info("TTS generation started: {} characters", len(cleaned_text))

    try:
        provider = GTTSProvider(language=settings.default_language or "en")
        generated_path = provider.synthesize_to_file(cleaned_text, output_path)

        if not generated_path.exists() or generated_path.stat().st_size == 0:
            raise TextToSpeechError("TTS provider did not create a valid audio file.")

        logger.info("TTS generation completed: {}", generated_path)
        return str(generated_path)
    except (ValueError, TextToSpeechError):
        logger.exception("TTS generation failed.")
        raise
    except Exception as exc:
        logger.exception("Unexpected TTS generation failure.")
        raise TextToSpeechError("Failed to synthesize speech.") from exc
