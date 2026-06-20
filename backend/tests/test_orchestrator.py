import pytest
from pydantic import ValidationError

from src.models.farmer import FarmerProfile
from src.models.request import FarmerRequest
from src.models.response import FarmerResponse
from src.orchestrator.conversation_manager import ConversationManager
from src.orchestrator.intent_router import IntentRouter
from src.utils.constants import (
    CLARIFICATION_QUESTION,
    INTENT_DISEASE,
    INTENT_FINANCE,
    INTENT_UNKNOWN,
    INTENT_WEATHER,
)
from src.utils.exceptions import SessionNotFoundError


def test_farmer_request_validates_non_empty_input() -> None:
    with pytest.raises(ValidationError):
        FarmerRequest(farmer_input="   ")


def test_farmer_request_auto_generates_ids_and_metadata() -> None:
    request = FarmerRequest(farmer_input="Meri fasal me keeda hai")

    assert request.request_id
    assert request.session_id
    assert request.metadata == {}


def test_farmer_response_confidence_bounds() -> None:
    with pytest.raises(ValidationError):
        FarmerResponse(
            request_id="request-1",
            response_text="Invalid confidence",
            intent=INTENT_DISEASE,
            confidence=1.5,
            source="test",
        )


def test_farmer_profile_defaults() -> None:
    profile = FarmerProfile()

    assert profile.farmer_id
    assert profile.preferred_language == "auto"
    assert profile.crops == []


def test_intent_router_detects_disease() -> None:
    result = IntentRouter().detect_intent("Tomato crop me keeda aur bimari hai")

    assert result["intent"] == INTENT_DISEASE
    assert result["confidence"] >= 0.5


def test_intent_router_detects_weather() -> None:
    result = IntentRouter().detect_intent("Aaj mausam aur barish ka kya haal hai")

    assert result["intent"] == INTENT_WEATHER
    assert result["confidence"] >= 0.5


def test_intent_router_detects_hinglish_finance() -> None:
    result = IntentRouter().detect_intent("Kisan loan yojana aur subsidy batao")

    assert result["intent"] == INTENT_FINANCE
    assert result["confidence"] >= 0.5


def test_intent_router_unknown_intent() -> None:
    result = IntentRouter().detect_intent("Namaste ji")

    assert result == {"intent": INTENT_UNKNOWN, "confidence": 0.0}


def test_intent_router_detects_crop_health_context_from_user_phrase() -> None:
    result = IntentRouter().detect_intent(
        "I need to know if I am doing something wrong, gives my potatoes a lot."
    )

    assert result["intent"] == INTENT_DISEASE
    assert result["confidence"] >= 0.5


def test_conversation_manager_creates_session() -> None:
    manager = ConversationManager()
    session_id = manager.create_session()

    assert session_id
    assert manager.get_session_history(session_id) == []


def test_conversation_manager_processes_request() -> None:
    manager = ConversationManager()
    session_id = manager.create_session()
    request = FarmerRequest(
        session_id=session_id,
        farmer_input="Meri mirchi me rog lag gaya hai",
    )

    response = manager.process_request(request)

    assert response.request_id == request.request_id
    assert response.intent == INTENT_DISEASE
    assert response.requires_followup is False
    assert response.source == "Disease Advisory Service"
    assert "Disease Service Placeholder" in response.response_text


def test_conversation_manager_generates_followup_for_low_confidence() -> None:
    manager = ConversationManager()
    session_id = manager.create_session()
    request = FarmerRequest(session_id=session_id, farmer_input="Mujhe madad chahiye")

    response = manager.process_request(request)

    assert response.intent == INTENT_UNKNOWN
    assert response.requires_followup is True
    assert response.followup_question == CLARIFICATION_QUESTION
    assert response.response_text == CLARIFICATION_QUESTION


def test_conversation_manager_retrieves_history() -> None:
    manager = ConversationManager()
    session_id = manager.create_session()
    request = FarmerRequest(session_id=session_id, farmer_input="Kal rain hogi kya")

    response = manager.process_request(request)
    history = manager.get_session_history(session_id)

    assert len(history) == 1
    assert history[0]["request"] == request
    assert history[0]["response"] == response


def test_conversation_manager_clears_session() -> None:
    manager = ConversationManager()
    session_id = manager.create_session()

    manager.clear_session(session_id)

    with pytest.raises(SessionNotFoundError):
        manager.get_session_history(session_id)


def test_conversation_manager_creates_missing_session_from_request() -> None:
    manager = ConversationManager()
    request = FarmerRequest(session_id="external-session", farmer_input="Mandi bhav batao")

    response = manager.process_request(request)

    assert response.intent == "market"
    assert len(manager.get_session_history("external-session")) == 1
