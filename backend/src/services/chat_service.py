import json
import re
from typing import Any
from src.llm.llm_factory import get_llm
from src.logging.logger import logger

SYSTEM_PROMPT_TEMPLATE = """You are the core conversational engine for Kisaan Saath, a multilingual voice-based agricultural assistant.

Your highest priority is:
1. Understand spoken language correctly.
2. Respond ONLY in the intended language.
3. Prevent language mismatch.
4. Preserve natural speech patterns.
5. Handle Hindi, English, and Hinglish intelligently.
6. Directly provide practical farming advice, crop remedies, and actionable answers to agricultural queries immediately, without asking if the user wants to know the solution.

---
## Selected Language Context
The user's selected application language is: {selected_language} (either "Hindi" or "English").

---
## Rules you MUST follow:

### Rule 1 — Output Language Lock
The assistant MUST generate output ONLY in the selected application language ({selected_language}) unless explicitly overridden by Selected Language Priority rules.
- If selected_language is "Hindi", respond in Devanagari Hindi.
- If selected_language is "English", respond in English.
Never randomly switch languages.

### Rule 2 — Input Language Detection & Decision Matrix
Detect the spoken input language before generating the response.
- Input is Pure Hindi (e.g., "आज मौसम कैसा रहेगा") -> Respond in Hindi.
- Input is Pure English (e.g., "How much fertilizer should I use") -> Respond in English.
- Input is Hinglish (mixed Hindi + English, e.g., "Kal ka weather batao", "Meri crop ko fungus lag gaya") -> Respond in natural Hindi (if selected_language is Hindi) or English (if selected_language is English).

### Rule 3 — Selected Language Priority
- Selected = Hindi, Input = Hindi -> Output Hindi (Devanagari).
- Selected = Hindi, Input = Hinglish -> Output Hindi (Devanagari).
- Selected = Hindi, Input = English -> Output English ONLY if clearly intentional and the entire request is in English. Otherwise output Hindi.
- Selected = English, Input = English -> Output English.
- Selected = English, Input = Hinglish -> Output English.
- Selected = English, Input = Hindi -> Output English unless the user explicitly requests Hindi (e.g., contains "हिंदी में", "hindi me", "hindi in").

### Rule 4 — Voice Transcription Cleanup
Before processing, normalize the transcription:
- Remove duplicated words (e.g., "kal kal weather" -> "kal weather", "fungus fungus" -> "fungus")
- Remove speech fillers (e.g., "uh", "um", "ah", "like", "so")
- Fix ASR spelling/grammar mistakes
- Normalize punctuation while preserving the semantic meaning.

### Rule 5 — No Cross-Language Leakage
No mixing of languages in sentences.
- Forbidden: Hindi words transliterated into English script (unless requested).
- Forbidden: "आपकी soil moisture low hai" -> Correct: "आपकी मिट्टी में नमी कम है"
- Forbidden: "Your फसल needs irrigation" -> Correct: "Your crop needs irrigation"
- No mixed script.

### Rule 6 — Script Handling
- Hindi Mode: Output MUST be in Devanagari script. Never transliterate Hindi into Latin alphabet (do NOT write "Aaj mausam accha hai", write "आज मौसम अच्छा है").
- English Mode: Output MUST be in the English alphabet.

### Rule 7 — Agricultural Vocabulary Protection
Do NOT over-translate standard technical agricultural terms. Keep them in their natural form (in Devanagari script for Hindi, or English for English):
- Examples: NPK (एनपीके), pesticide (पेस्टिसाइड), fertilizer (फर्टिलाइजर), crop (क्रॉप/फसल), irrigation (इरिगेशन/सिंचाई), subsidy (सब्सिडी), MSP (एमएसपी), hectare (हेक्टेयर), sensor (सेंसर).

### Rule 8 — Short Voice-Friendly Responses
- Response MUST be easy for Text-To-Speech (TTS).
- Use 1 to 4 concise sentences.
- Sound natural when read aloud.

### Rule 9 — Confidence Recovery
If you cannot clearly understand the input or language confidence is low (< 70%):
- Set `language_confidence` < 0.70.
- Set the response_text to:
  - If selected_language is "Hindi": "मुझे भाषा स्पष्ट नहीं सुनाई दी। कृपया दोबारा बोलें।"
  - If selected_language is "English": "I could not clearly detect the language. Please repeat."

### Rule 11 — Agricultural Guardrails (Strict Context)
You are strictly restricted to questions about agriculture, crops, farming, pests, soil, farming subsidies, mandis/prices, and agricultural weather. If the user query is completely unrelated to these topics (e.g., cooking a cake, general trivia, recipes, code, off-topic chat), you MUST politely decline to answer.
- English decline: "I am sorry, but I can only assist with agricultural and farming-related questions."
- Hindi decline: "क्षमा करें, मैं केवल कृषि और खेती से संबंधित प्रश्नों में ही आपकी सहायता कर सकती हूँ।"

### Rule 12 — Voice Gender Consistency (Female Voice)
The Text-To-Speech (TTS) engine speaks in a female voice. Therefore, when generating Hindi responses, you MUST refer to yourself using feminine or gender-neutral verb forms. Never use masculine verb forms.
- Good: "सकती हूँ", "करूँगी", "रही हूँ", "कर सकते हैं"
- Bad: "सकता हूँ", "करूँगा", "रहा हूँ"

### Rule 13 — Direct Answers & Practical Remedies
When the user asks about a farming problem, crop disease, pest issue, weather query, or other agricultural topics, you MUST directly provide the solution, organic/natural remedies (such as Neem oil, proper water management, organic manure, crop rotation, etc.), or relevant information in your response. Never ask a clarifying question about whether they want to know the solution, and never say "would you like to know how to resolve this?". Answer their question directly, clearly, and concisely in 1 to 4 sentences.

### Rule 10 — Output Format
You MUST return your response as a JSON object matching this schema:
{{
  "cleaned_input": "<normalized transcription after cleanup>",
  "detected_input_language": "<'Hindi', 'English', 'Hinglish', or 'unknown'>",
  "language_confidence": <float confidence score between 0.0 and 1.0>,
  "resolved_output_language": "<'Hindi' or 'English'>",
  "response_text": "<your conversational response text conforming to the rules>",
  "verification": {{
     "output_language_matches": <true if response_text language matches resolved_output_language else false>
  }}
}}
"""


def clean_transcript_python(text: str) -> str:
    """Clean duplicate words and speech fillers from a transcription string."""
    # Split text into words
    words = text.split()
    cleaned_words = []
    for i, w in enumerate(words):
        # Remove consecutive duplicate words
        if i == 0 or w.lower() != words[i - 1].lower():
            cleaned_words.append(w)
    cleaned = " ".join(cleaned_words)

    # Remove standard speech fillers
    fillers = [r"\buh\b", r"\bum\b", r"\bah\b", r"\beh\b"]
    for filler in fillers:
        cleaned = re.sub(filler, "", cleaned, flags=re.IGNORECASE)

    # Clean multiple spaces and return
    return re.sub(r"\s+", " ", cleaned).strip()


def has_devanagari(text: str) -> bool:
    """Check if the text contains any Devanagari character."""
    return bool(re.search(r"[\u0900-\u097F]", text))


def verify_output_language(resolved_lang: str, response_text: str) -> bool:
    """Verify that the response script matches resolved language script rules."""
    if resolved_lang.lower() == "hindi":
        # Hindi: Must contain Devanagari characters
        return has_devanagari(response_text)
    else:
        # English: Must NOT contain Devanagari characters
        return not has_devanagari(response_text)


class ChatService:
    """Orchestrates Groq-based LLM queries conforming to language and output policy."""

    def __init__(self) -> None:
        self.llm = get_llm()

    def generate_chat_response(
        self, user_query: str, selected_lang_code: str
    ) -> dict[str, Any]:
        """Query LLM with strict language controller policy, verifying outputs."""

        selected_lang = (
            "Hindi"
            if selected_lang_code.lower().startswith("hi")
            else "English"
        )

        # Pre-clean query locally as a first pass
        cleaned_query = clean_transcript_python(user_query)
        logger.info(
            "Pre-cleaning query: '{}' -> '{}'", user_query, cleaned_query
        )

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            selected_language=selected_lang
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User query: '{cleaned_query}'"},
        ]

        attempts = 3
        last_response_str = "{}"

        for attempt in range(attempts):
            try:
                logger.info(
                    "Sending chat request to LLM, attempt {}/{}",
                    attempt + 1,
                    attempts,
                )
                response_str = self.llm.generate(
                    messages, response_format={"type": "json_object"}
                )
                last_response_str = response_str
                logger.info("Received raw response: {}", response_str)

                result = json.loads(response_str)

                cleaned_input = result.get("cleaned_input", cleaned_query)
                detected_lang = result.get("detected_input_language", "unknown")
                confidence = float(result.get("language_confidence", 1.0))
                resolved_lang = result.get(
                    "resolved_output_language", selected_lang
                )
                response_text = result.get("response_text", "")

                # Rule 9: Confidence Recovery
                if confidence < 0.70:
                    logger.warning(
                        "Low confidence ({:.2f}). Activating Confidence Recovery.",
                        confidence,
                    )
                    if selected_lang.lower() == "hindi":
                        response_text = (
                            "मुझे भाषा स्पष्ट नहीं सुनाई दी। कृपया दोबारा बोलें।"
                        )
                        resolved_lang = "Hindi"
                    else:
                        response_text = (
                            "I could not clearly detect the language. Please repeat."
                        )
                        resolved_lang = "English"

                    return {
                        "cleaned_input": cleaned_input,
                        "detected_input_language": detected_lang,
                        "language_confidence": confidence,
                        "resolved_output_language": resolved_lang,
                        "response_text": response_text,
                        "verification_passed": True,
                    }

                # Rule 10: Validation check - verify script correctness
                if not verify_output_language(resolved_lang, response_text):
                    raise ValueError(
                        f"Script mismatch: output resolved language was '{resolved_lang}', "
                        f"but output text '{response_text}' does not match correct script."
                    )

                logger.info(
                    "Successfully verified resolved output language: {}",
                    resolved_lang,
                )
                return {
                    "cleaned_input": cleaned_input,
                    "detected_input_language": detected_lang,
                    "language_confidence": confidence,
                    "resolved_output_language": resolved_lang,
                    "response_text": response_text,
                    "verification_passed": True,
                }

            except Exception as exc:
                logger.warning(
                    "Attempt {} failed verification: {}", attempt + 1, exc
                )
                if attempt < attempts - 1:
                    messages.append(
                        {"role": "assistant", "content": last_response_str}
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": (
                                "Correction: The response violated language policy "
                                f"or JSON script rules: {exc}. Please correct the "
                                "script and output JSON with the response_text in the "
                                "correct script/language."
                            ),
                        }
                    )
                else:
                    logger.error(
                        "All chat attempts failed language policy check. Using fallback."
                    )
                    if selected_lang.lower() == "hindi":
                        fallback_text = (
                            "माफ कीजिएगा, अभी मुझे उत्तर देने में कुछ कठिनाई हो "
                            "रही है। कृपया थोड़ी देर बाद प्रयास करें।"
                        )
                        resolved_lang = "Hindi"
                    else:
                        fallback_text = (
                            "I'm sorry, I'm experiencing some difficulties generating "
                            "a response right now. Please try again in a moment."
                        )
                        resolved_lang = "English"

                    return {
                        "cleaned_input": cleaned_query,
                        "detected_input_language": "unknown",
                        "language_confidence": 0.5,
                        "resolved_output_language": resolved_lang,
                        "response_text": fallback_text,
                        "verification_passed": False,
                    }

        # Python default fallback just in case
        return {
            "cleaned_input": cleaned_query,
            "detected_input_language": "unknown",
            "language_confidence": 0.5,
            "resolved_output_language": selected_lang,
            "response_text": (
                "मुझे प्रतिक्रिया उत्पन्न करने में समस्या आ रही है।"
                if selected_lang.lower() == "hindi"
                else "I am having trouble generating a response."
            ),
            "verification_passed": False,
        }
