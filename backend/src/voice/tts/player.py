from pathlib import Path


def load_audio(audio_path: str) -> bytes:
    """Load generated audio bytes for Streamlit playback."""

    if not audio_path or not audio_path.strip():
        raise ValueError("Audio path is required.")

    path = Path(audio_path)

    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if not path.is_file():
        raise ValueError(f"Audio path is not a file: {audio_path}")

    return path.read_bytes()
