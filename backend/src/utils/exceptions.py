class KisanSaathiError(Exception):
    """Base exception for KisanSaathi domain errors."""


class ConversationError(KisanSaathiError):
    """Raised when conversation orchestration fails."""


class SessionNotFoundError(ConversationError):
    """Raised when a requested conversation session does not exist."""
