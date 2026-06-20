import pytest
from unittest.mock import MagicMock
from src.services.chat_service import (
    ChatService,
    clean_transcript_python,
    verify_output_language,
    has_devanagari,
)


def test_clean_transcript_python() -> None:
    # Rule 4: transcription cleanup tests
    assert clean_transcript_python("kal kal weather bata") == "kal weather bata"
    assert (
        clean_transcript_python("mere khet me fungus fungus aa gaya")
        == "mere khet me fungus aa gaya"
    )
    assert (
        clean_transcript_python("uh crop is um dying so yellow")
        == "crop is dying so yellow"
    )


def test_has_devanagari() -> None:
    assert has_devanagari("आज तापमान ३४ डिग्री रहेगा") is True
    assert has_devanagari("Today's temperature") is False
    assert has_devanagari("crop") is False


def test_verify_output_language() -> None:
    assert verify_output_language("Hindi", "आज मौसम अच्छा है") is True
    assert verify_output_language("Hindi", "Aaj mausam accha hai") is False
    assert verify_output_language("English", "Your crop needs water") is True
    assert verify_output_language("English", "आपकी फसल") is False


def test_chat_service_success(monkeypatch: pytest.MonkeyPatch) -> None:
    # Mock LLM response
    mock_llm = MagicMock()
    mock_llm.generate.return_value = """{
        "cleaned_input": "kal weather kaisa hoga",
        "detected_input_language": "Hinglish",
        "language_confidence": 0.95,
        "resolved_output_language": "Hindi",
        "response_text": "कल बारिश होने की संभावना है।",
        "verification": {
            "output_language_matches": true
        }
    }"""

    monkeypatch.setattr("src.services.chat_service.get_llm", lambda: mock_llm)

    service = ChatService()
    res = service.generate_chat_response("kal kal weather kaisa hoga", "hi")

    assert res["resolved_output_language"] == "Hindi"
    assert "कल बारिश" in res["response_text"]
    assert res["verification_passed"] is True


def test_chat_service_confidence_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock LLM with low confidence
    mock_llm = MagicMock()
    mock_llm.generate.return_value = """{
        "cleaned_input": "...",
        "detected_input_language": "unknown",
        "language_confidence": 0.40,
        "resolved_output_language": "English",
        "response_text": "...",
        "verification": {
            "output_language_matches": false
        }
    }"""

    monkeypatch.setattr("src.services.chat_service.get_llm", lambda: mock_llm)

    service = ChatService()
    res = service.generate_chat_response("abcd", "en")

    assert res["resolved_output_language"] == "English"
    assert (
        "I could not clearly detect the language" in res["response_text"]
    )


def test_chat_service_script_mismatch_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # First response fails script check (Hindi expected, gets English alphabet)
    # Second response passes script check
    responses = [
        """{
            "cleaned_input": "kisan yojana",
            "detected_input_language": "Hinglish",
            "language_confidence": 0.90,
            "resolved_output_language": "Hindi",
            "response_text": "Kisan yojana ke baare me...",
            "verification": {
                "output_language_matches": true
            }
        }""",
        """{
            "cleaned_input": "kisan yojana",
            "detected_input_language": "Hinglish",
            "language_confidence": 0.90,
            "resolved_output_language": "Hindi",
            "response_text": "किसान योजना के तहत आपको मदद मिलेगी।",
            "verification": {
                "output_language_matches": true
            }
        }""",
    ]

    mock_llm = MagicMock()
    mock_llm.generate.side_effect = responses

    monkeypatch.setattr("src.services.chat_service.get_llm", lambda: mock_llm)

    service = ChatService()
    res = service.generate_chat_response("kisan yojana", "hi")

    assert res["resolved_output_language"] == "Hindi"
    assert "किसान योजना" in res["response_text"]
    assert mock_llm.generate.call_count == 2
