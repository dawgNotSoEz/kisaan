from dataclasses import dataclass

from src.logging.logger import logger
from src.utils.constants import (
    INTENT_DISEASE,
    INTENT_EDUCATION,
    INTENT_FINANCE,
    INTENT_MARKET,
    INTENT_SEED,
    INTENT_UNKNOWN,
    INTENT_WEATHER,
)
from src.utils.helpers import normalize_text


@dataclass(frozen=True)
class IntentMatch:
    """Intent match result."""

    intent: str
    confidence: float

    def as_dict(self) -> dict[str, float | str]:
        """Return a dictionary compatible with downstream callers."""

        return {"intent": self.intent, "confidence": self.confidence}


class IntentRouter:
    """Lightweight rule-based intent router for Phase 2 orchestration."""

    _CROP_TERMS: tuple[str, ...] = (
        "aloo",
        "bajra",
        "brinjal",
        "chilli",
        "cotton",
        "crop",
        "crops",
        "fasal",
        "gehu",
        "mirchi",
        "paddy",
        "potato",
        "potatoes",
        "rice",
        "tomato",
        "wheat",
    )
    _CROP_HEALTH_TERMS: tuple[str, ...] = (
        "damage",
        "damaged",
        "dying",
        "fungus",
        "issue",
        "problem",
        "rot",
        "rotten",
        "spot",
        "spots",
        "weak",
        "wilting",
        "wrong",
        "yellow",
    )

    _KEYWORDS: dict[str, tuple[str, ...]] = {
        INTENT_DISEASE: (
            "disease",
            "pest",
            "infection",
            "bimari",
            "rog",
            "keeda",
        ),
        INTENT_WEATHER: (
            "rain",
            "weather",
            "mausam",
            "barish",
        ),
        INTENT_FINANCE: (
            "subsidy",
            "loan",
            "yojana",
            "scheme",
        ),
        INTENT_SEED: (
            "seed",
            "beej",
            "variety",
        ),
        INTENT_MARKET: (
            "mandi",
            "price",
            "market",
            "bhav",
        ),
        INTENT_EDUCATION: (
            "natural farming",
            "organic",
            "jaivik",
            "multilevel",
        ),
    }

    def detect_intent(self, farmer_input: str) -> dict[str, float | str]:
        """Detect intent using deterministic keyword matching.

        Args:
            farmer_input: Farmer utterance or transcript.

        Returns:
            Dictionary with detected intent and heuristic confidence.
        """

        normalized_input = normalize_text(farmer_input)
        if not normalized_input:
            result = IntentMatch(intent=INTENT_UNKNOWN, confidence=0.0)
            logger.info("Intent detection completed: {}", result.as_dict())
            return result.as_dict()

        scores = {
            intent: self._score_intent(normalized_input, keywords)
            for intent, keywords in self._KEYWORDS.items()
        }
        best_intent, best_score = max(scores.items(), key=lambda item: item[1])

        if best_score == 0:
            result = self._detect_contextual_crop_intent(normalized_input)
        else:
            result = IntentMatch(intent=best_intent, confidence=best_score)

        logger.info("Intent detection completed: {}", result.as_dict())
        return result.as_dict()

    def _score_intent(self, normalized_input: str, keywords: tuple[str, ...]) -> float:
        matched_keywords = [
            keyword for keyword in keywords if self._keyword_matches(normalized_input, keyword)
        ]

        if not matched_keywords:
            return 0.0

        exact_boost = 0.15 if any(keyword == normalized_input for keyword in matched_keywords) else 0.0
        coverage = min(len(matched_keywords), 3) * 0.18
        return min(0.55 + coverage + exact_boost, 0.95)

    def _detect_contextual_crop_intent(self, normalized_input: str) -> IntentMatch:
        has_crop_context = any(
            self._keyword_matches(normalized_input, crop_term)
            for crop_term in self._CROP_TERMS
        )
        has_crop_health_context = any(
            self._keyword_matches(normalized_input, health_term)
            for health_term in self._CROP_HEALTH_TERMS
        )

        if has_crop_context and has_crop_health_context:
            return IntentMatch(intent=INTENT_DISEASE, confidence=0.58)

        return IntentMatch(intent=INTENT_UNKNOWN, confidence=0.0)

    @staticmethod
    def _keyword_matches(normalized_input: str, keyword: str) -> bool:
        normalized_keyword = normalize_text(keyword)
        if " " in normalized_keyword:
            return normalized_keyword in normalized_input

        words = normalized_input.split()
        return normalized_keyword in words
