from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.utils.helpers import utc_now


class FarmerResponse(BaseModel):
    """Standardized response produced by the conversation orchestration layer."""

    request_id: str
    response_text: str
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    requires_followup: bool = False
    followup_question: str | None = None
    source: str
    timestamp: datetime = Field(default_factory=utc_now)

    @field_validator("response_text", "intent", "source")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        """Validate required response text fields."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Response fields cannot be empty.")
        return cleaned
