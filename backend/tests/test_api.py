import base64
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app

client = TestClient(app)


def test_api_get_crops() -> None:
    res = client.get("/api/v1/crops?lang=hi")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert data[0]["id"] == "tomato"
    assert "टमाटर" in data[0]["name"]


def test_api_get_symptoms() -> None:
    res = client.get("/api/v1/symptoms?crop_id=tomato&lang=en")
    assert res.status_code == 200
    data = res.json()
    assert "parts" in data
    assert "observations" in data
    assert data["parts"][0]["id"] == "leaves"


def test_api_get_remedy() -> None:
    res = client.get(
        "/api/v1/remedy?crop_id=tomato&part=leaves&observation=spots&lang=ta"
    )
    assert res.status_code == 200
    data = res.json()
    assert "disease_name" in data
    assert "organic_management" in data
    assert "இலைக்கருகல்" in data["disease_name"]


@patch("main.chat_service")
@patch("main.synthesize")
def test_api_chat(
    mock_synthesize: MagicMock, mock_chat_service: MagicMock, tmp_path: Path
) -> None:
    mock_chat_service.generate_chat_response.return_value = {
        "response_text": "किसान भाइयों, अपनी फसल में नीम तेल डालें।",
        "resolved_output_language": "Hindi",
        "cleaned_input": "mirchi me rog",
        "verification_passed": True,
    }

    dummy_audio = tmp_path / "tts.mp3"
    dummy_audio.write_bytes(b"audio-bytes")
    mock_synthesize.return_value = str(dummy_audio)

    payload = {"query": "mirchi me rog", "lang": "hi"}
    res = client.post("/api/v1/chat", json=payload)

    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "किसान भाइयों, अपनी फसल में नीम तेल डालें।"
    assert data["audio_base64"] == base64.b64encode(b"audio-bytes").decode(
        "utf-8"
    )


@patch("main.transcribe")
@patch("main.chat_service")
@patch("main.synthesize")
def test_api_chat_audio(
    mock_synthesize: MagicMock,
    mock_chat_service: MagicMock,
    mock_transcribe: MagicMock,
    tmp_path: Path,
) -> None:
    mock_transcribe.return_value = "mirchi me rog"
    mock_chat_service.generate_chat_response.return_value = {
        "response_text": "किसान भाइयों, अपनी फसल में नीम तेल डालें।",
        "resolved_output_language": "Hindi",
        "cleaned_input": "mirchi me rog",
        "verification_passed": True,
    }

    dummy_audio = tmp_path / "tts.mp3"
    dummy_audio.write_bytes(b"audio-bytes")
    mock_synthesize.return_value = str(dummy_audio)

    fake_audio = tmp_path / "input.webm"
    fake_audio.write_bytes(b"webm-bytes")

    with open(fake_audio, "rb") as f:
        res = client.post(
            "/api/v1/chat/audio",
            files={"file": ("input.webm", f, "audio/webm")},
            data={"lang": "hi"},
        )

    assert res.status_code == 200
    data = res.json()
    assert data["transcription"] == "mirchi me rog"
    assert data["answer"] == "किसान भाइयों, अपनी फसल में नीम तेल डालें।"
    assert data["audio_base64"] == base64.b64encode(b"audio-bytes").decode(
        "utf-8"
    )
