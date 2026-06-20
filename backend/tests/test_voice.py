from pathlib import Path

import pytest

from src.voice.stt import whisper_loader
from src.voice.stt.ffmpeg import FFmpegNotFoundError, ensure_ffmpeg_available
from src.voice.stt.transcriber import TranscriptionError, transcribe
from src.voice.tts.player import load_audio
from src.voice.tts.synthesizer import synthesize


def test_whisper_loader_uses_configured_model(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    expected_model = object()

    def fake_load_model(model_name: str) -> object:
        calls.append(model_name)
        return expected_model

    whisper_loader._load_model.cache_clear()
    monkeypatch.setattr(whisper_loader.settings, "whisper_model", "tiny")
    monkeypatch.setattr(whisper_loader.whisper, "load_model", fake_load_model)

    assert whisper_loader.load_whisper() is expected_model
    assert whisper_loader.load_whisper() is expected_model
    assert calls == ["tiny"]

    whisper_loader._load_model.cache_clear()


def test_audio_transcription_missing_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        transcribe("missing-audio-file.wav")


def test_audio_transcription_empty_result_raises(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audio_file = tmp_path / "voice.wav"
    audio_file.write_bytes(b"audio")

    class FakeModel:
        def transcribe(self, *_args: object, **_kwargs: object) -> dict[str, str]:
            return {"text": "   "}

    monkeypatch.setattr(
        "src.voice.stt.transcriber.load_whisper",
        lambda: FakeModel(),
    )
    monkeypatch.setattr(
        "src.voice.stt.transcriber.ensure_ffmpeg_available",
        lambda: "ffmpeg",
    )

    with pytest.raises(TranscriptionError):
        transcribe(str(audio_file))


def test_ffmpeg_failure_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.voice.stt.ffmpeg.shutil.which", lambda _name: None)
    monkeypatch.setattr("src.voice.stt.ffmpeg._install_imageio_ffmpeg_shim", lambda: None)

    with pytest.raises(FFmpegNotFoundError, match="pip install imageio-ffmpeg"):
        ensure_ffmpeg_available()


def test_empty_tts_input_validation() -> None:
    with pytest.raises(ValueError):
        synthesize("")


def test_audio_loading(tmp_path: Path) -> None:
    audio_file = tmp_path / "response.mp3"
    audio_file.write_bytes(b"mp3-bytes")

    assert load_audio(str(audio_file)) == b"mp3-bytes"


def test_successful_tts_generation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeProvider:
        def __init__(self, language: str = "en") -> None:
            self.language = language

        def synthesize_to_file(self, text: str, output_path: Path) -> Path:
            output_path.write_bytes(f"audio:{self.language}:{text}".encode("utf-8"))
            return output_path

    monkeypatch.setattr("src.voice.tts.synthesizer.GTTSProvider", FakeProvider)

    output = synthesize("Hello farmer")

    assert Path(output).exists()
    assert Path(output).read_bytes().startswith(b"audio:")
