from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from src.utils.helpers import generate_id, utc_now


class FarmerRequest(BaseModel):
    """Standardized request entering the conversation orchestration layer."""

    request_id: str = Field(default_factory=generate_id)
    session_id: str = Field(default_factory=generate_id)
    farmer_input: str
    detected_language: str = "auto"
    timestamp: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("farmer_input")
    @classmethod
    def validate_farmer_input(cls, value: str) -> str:
        """Validate and normalize farmer input."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Farmer input cannot be empty.")
        return cleaned

    @field_validator("detected_language")
    @classmethod
    def validate_detected_language(cls, value: str) -> str:
        """Validate language marker."""

        cleaned = value.strip()
        if not cleaned:
            return "auto"
        return cleaned
