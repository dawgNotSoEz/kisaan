from typing import Final


INTENT_DISEASE: Final[str] = "disease"
INTENT_EDUCATION: Final[str] = "education"
INTENT_FINANCE: Final[str] = "finance"
INTENT_MARKET: Final[str] = "market"
INTENT_SEED: Final[str] = "seed"
INTENT_WEATHER: Final[str] = "weather"
INTENT_UNKNOWN: Final[str] = "unknown"

SUPPORTED_INTENTS: Final[tuple[str, ...]] = (
    INTENT_DISEASE,
    INTENT_EDUCATION,
    INTENT_FINANCE,
    INTENT_MARKET,
    INTENT_SEED,
    INTENT_WEATHER,
    INTENT_UNKNOWN,
)

FOLLOWUP_CONFIDENCE_THRESHOLD: Final[float] = 0.50

CLARIFICATION_QUESTION: Final[str] = (
    "I couldn't fully understand your farming query. Is it related to disease, "
    "weather, seeds, markets, finance, or natural farming education?"
)

DOMAIN_SERVICE_PLACEHOLDERS: Final[dict[str, tuple[str, str]]] = {
    INTENT_DISEASE: (
        "Disease Advisory Service",
        "[Disease Service Placeholder] This request would be routed to disease advisory.",
    ),
    INTENT_WEATHER: (
        "Weather Intelligence Service",
        "[Weather Service Placeholder] This request would be routed to weather intelligence.",
    ),
    INTENT_FINANCE: (
        "Financial Guidance Service",
        "[Finance Service Placeholder] This request would be routed to financial guidance.",
    ),
    INTENT_MARKET: (
        "Market Intelligence Service",
        "[Market Service Placeholder] This request would be routed to market intelligence.",
    ),
    INTENT_SEED: (
        "Seed Guidance Service",
        "[Seed Service Placeholder] This request would be routed to seed guidance.",
    ),
    INTENT_EDUCATION: (
        "Natural Farming Education Service",
        "[Education Service Placeholder] This request would be routed to natural farming education.",
    ),
}
