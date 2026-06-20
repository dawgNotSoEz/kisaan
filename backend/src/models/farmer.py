from pydantic import BaseModel, Field

from src.utils.helpers import generate_id


class FarmerProfile(BaseModel):
    """Farmer profile for future personalization."""

    farmer_id: str = Field(default_factory=generate_id)
    preferred_language: str = "auto"
    state: str | None = None
    district: str | None = None
    crops: list[str] = Field(default_factory=list)
    farm_size: float | None = Field(default=None, ge=0.0)
