import os
import shutil
import tempfile
from pathlib import Path

from src.logging.logger import logger


class FFmpegNotFoundError(RuntimeError):
    """Raised when Whisper cannot access an ffmpeg executable."""


def _install_imageio_ffmpeg_shim() -> str | None:
    try:
        import imageio_ffmpeg
    except ImportError:
        return None

    bundled_ffmpeg = Path(imageio_ffmpeg.get_ffmpeg_exe())
    if not bundled_ffmpeg.exists():
        return None

    shim_dir = Path(tempfile.gettempdir()) / "kisan_saathi_ffmpeg"
    shim_dir.mkdir(parents=True, exist_ok=True)

    executable_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    shim_path = shim_dir / executable_name

    if not shim_path.exists():
        shutil.copy2(bundled_ffmpeg, shim_path)

    current_path = os.environ.get("PATH", "")
    shim_dir_text = str(shim_dir)
    if shim_dir_text not in current_path.split(os.pathsep):
        os.environ["PATH"] = shim_dir_text + os.pathsep + current_path

    return str(shim_path)


def ensure_ffmpeg_available() -> str:
    """Ensure Whisper can invoke ffmpeg by name."""

    existing_ffmpeg = shutil.which("ffmpeg")
    if existing_ffmpeg:
        return existing_ffmpeg

    shimmed_ffmpeg = _install_imageio_ffmpeg_shim()
    if shimmed_ffmpeg:
        logger.info("Using bundled ffmpeg for Whisper: {}", shimmed_ffmpeg)
        return shimmed_ffmpeg

    raise FFmpegNotFoundError(
        "ffmpeg is required for speech transcription but was not found. "
        "Install ffmpeg and add it to PATH, or run `pip install imageio-ffmpeg`."
    )
