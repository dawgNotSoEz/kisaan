import re
from datetime import datetime, timezone
from uuid import uuid4


def generate_id() -> str:
    """Generate a stable unique identifier string."""

    return str(uuid4())


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""

    return datetime.now(timezone.utc)


def normalize_text(text: str) -> str:
    """Normalize user text for lightweight rule matching."""

    lowered = text.casefold().strip()
    without_punctuation = re.sub(r"[^\w\s]", " ", lowered)
    return re.sub(r"\s+", " ", without_punctuation).strip()
