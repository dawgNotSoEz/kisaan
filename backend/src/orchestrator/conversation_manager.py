from src.logging.logger import logger
from src.models.request import FarmerRequest
from src.models.response import FarmerResponse
from src.orchestrator.intent_router import IntentRouter
from src.utils.constants import (
    CLARIFICATION_QUESTION,
    DOMAIN_SERVICE_PLACEHOLDERS,
    FOLLOWUP_CONFIDENCE_THRESHOLD,
    INTENT_UNKNOWN,
)
from src.utils.exceptions import SessionNotFoundError
from src.utils.helpers import generate_id


ConversationTurn = dict[str, FarmerRequest | FarmerResponse]


class ConversationManager:
    """Coordinates farmer requests, intent routing, and response construction."""

    def __init__(self, intent_router: IntentRouter | None = None) -> None:
        self._intent_router = intent_router or IntentRouter()
        self._sessions: dict[str, list[ConversationTurn]] = {}

    def create_session(self) -> str:
        """Create a new in-memory conversation session."""

        session_id = generate_id()
        self._sessions[session_id] = []
        logger.info("Session created: {}", session_id)
        return session_id

    def process_request(self, request: FarmerRequest) -> FarmerResponse:
        """Process a farmer request and append the turn to session history.

        Args:
            request: Validated farmer request model.

        Returns:
            Standardized farmer response.
        """

        if request.session_id not in self._sessions:
            self._sessions[request.session_id] = []
            logger.info("Session created from incoming request: {}", request.session_id)

        logger.info(
            "Incoming request: request_id={}, session_id={}",
            request.request_id,
            request.session_id,
        )

        route = self._intent_router.detect_intent(request.farmer_input)
        intent = str(route["intent"])
        confidence = float(route["confidence"])
        logger.info(
            "Intent detected: request_id={}, intent={}, confidence={}",
            request.request_id,
            intent,
            confidence,
        )

        response = self._build_response(request, intent, confidence)
        self._sessions[request.session_id].append(
            {
                "request": request,
                "response": response,
            }
        )
        return response

    def get_session_history(self, session_id: str) -> list[ConversationTurn]:
        """Return conversation history for a session."""

        self._ensure_session_exists(session_id)
        return list(self._sessions[session_id])

    def clear_session(self, session_id: str) -> None:
        """Clear and remove a conversation session."""

        self._ensure_session_exists(session_id)
        del self._sessions[session_id]
        logger.info("Session cleared: {}", session_id)

    def _build_response(
        self,
        request: FarmerRequest,
        intent: str,
        confidence: float,
    ) -> FarmerResponse:
        if confidence < FOLLOWUP_CONFIDENCE_THRESHOLD or intent == INTENT_UNKNOWN:
            logger.info(
                "Follow-up triggered: request_id={}, confidence={}",
                request.request_id,
                confidence,
            )
            return FarmerResponse(
                request_id=request.request_id,
                response_text=CLARIFICATION_QUESTION,
                intent=INTENT_UNKNOWN,
                confidence=confidence,
                requires_followup=True,
                followup_question=CLARIFICATION_QUESTION,
                source="Conversation Orchestrator",
            )

        service_name, response_text = DOMAIN_SERVICE_PLACEHOLDERS[intent]
        return FarmerResponse(
            request_id=request.request_id,
            response_text=response_text,
            intent=intent,
            confidence=confidence,
            requires_followup=False,
            followup_question=None,
            source=service_name,
        )

    def _ensure_session_exists(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(f"Conversation session not found: {session_id}")
