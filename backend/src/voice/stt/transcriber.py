import os
from pathlib import Path
from typing import Any

from src.config.settings import settings
from src.logging.logger import logger
from src.voice.stt.ffmpeg import ensure_ffmpeg_available
from src.voice.stt.whisper_loader import load_whisper


class TranscriptionError(RuntimeError):
    """Raised when speech-to-text processing fails."""


def _extract_text(result: Any) -> str:
    if not isinstance(result, dict) or "text" not in result:
        raise TranscriptionError("Whisper returned an invalid transcription result.")

    text = str(result["text"]).strip()
    if not text:
        raise TranscriptionError("Whisper returned an empty transcript.")

    return text


def transcribe(audio_path: str, language: str | None = None) -> str:
    """Convert recorded audio to text using Groq Whisper API (preferred) or local Whisper."""

    path = Path(audio_path)

    if not audio_path or not str(audio_path).strip():
        raise ValueError("Audio path is required for transcription.")

    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if not path.is_file():
        raise ValueError(f"Audio path is not a file: {audio_path}")

    logger.info("Transcription started for file: {}", path)

    # Convert language code to ISO-639-1 (e.g. 'hi-IN' -> 'hi')
    whisper_lang = None
    if language:
        lang_code = language.split("-")[0].lower()
        if lang_code in ["hi", "en", "ta", "te", "mr"]:
            whisper_lang = lang_code

    # 1. Attempt Groq Hosted Whisper API first if API key is present
    api_key = (
        settings.groq_api_key
        or settings.openai_api_key
        or os.getenv("GROQ_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if api_key:
        logger.info("Using Groq Hosted Whisper API for transcription. Language target: {}", whisper_lang)
        try:
            from openai import OpenAI
            base_url = settings.groq_api_url or "https://api.groq.com/openai/v1"
            client = OpenAI(api_key=api_key, base_url=base_url)

            with open(path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    language=whisper_lang,
                    temperature=0.0,
                )
                transcript = transcription.text.strip()
                if not transcript:
                    raise TranscriptionError("Groq Whisper API returned an empty transcript.")
                logger.info("Transcription completed via Groq API: {} characters", len(transcript))
                return transcript
        except Exception as exc:
            logger.warning("Groq Hosted Whisper API failed: {}. Falling back to local.", exc)

    # 2. Fall back to local Whisper model
    try:
        ensure_ffmpeg_available()
        model = load_whisper()
        result = model.transcribe(
            str(path),
            fp16=False,
            language=whisper_lang,
            task="transcribe",
        )
        transcript = _extract_text(result)
        logger.info("Transcription completed via local Whisper: {} characters", len(transcript))
        return transcript
    except (FileNotFoundError, ValueError, TranscriptionError):
        logger.exception("Transcription failed for audio file: {}", path)
        raise
    except Exception as exc:
        logger.exception("Unexpected transcription failure for audio file: {}", path)
        raise TranscriptionError("Failed to transcribe audio.") from exc
