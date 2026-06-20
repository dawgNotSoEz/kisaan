import base64
import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.services.disease.service import get_crops, get_symptoms, get_remedy
from src.services.chat_service import ChatService
from src.voice.stt.transcriber import transcribe
from src.voice.tts.synthesizer import synthesize
from src.logging.logger import logger

app = FastAPI(title="KisanSaathi Backend", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_service = ChatService()


@app.get("/api/v1/crops")
async def api_get_crops(lang: str = "en"):
    return get_crops(lang)


@app.get("/api/v1/symptoms")
async def api_get_symptoms(crop_id: str, lang: str = "en"):
    return get_symptoms(crop_id, lang)


@app.get("/api/v1/remedy")
async def api_get_remedy(
    crop_id: str, part: str, observation: str, lang: str = "en"
):
    return get_remedy(crop_id, part, observation, lang)


@app.post("/api/v1/chat")
async def api_chat(payload: dict):
    query = payload.get("query", "")
    lang = payload.get("lang", "en")

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        response_data = chat_service.generate_chat_response(query, lang)
        answer = response_data["response_text"]

        # Generate speech audio (Rule 10 pipeline)
        audio_base64 = ""
        try:
            tts_path = synthesize(answer)
            if os.path.exists(tts_path):
                with open(tts_path, "rb") as f:
                    audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                try:
                    os.unlink(tts_path)
                except Exception:
                    pass
        except Exception as tts_err:
            logger.exception("Failed to synthesize TTS for chat: {}", tts_err)

        return {
            "transcription": query,
            "answer": answer,
            "audio_base64": audio_base64,
        }
    except Exception as exc:
        logger.exception("Chat endpoint failed: {}", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/v1/chat/audio")
async def api_chat_audio(file: UploadFile = File(...), lang: str = Form(...)):
    try:
        # Save uploaded audio file to temp file
        with tempfile.NamedTemporaryFile(
            suffix=".webm", delete=False
        ) as temp_audio:
            temp_path = Path(temp_audio.name)
            content = await file.read()
            temp_audio.write(content)

        # 1. Speech to Text (Whisper)
        try:
            transcription = transcribe(str(temp_path), language=lang)
        finally:
            # Clean up uploaded audio temp file
            try:
                os.unlink(temp_path)
            except Exception:
                pass

        if not transcription.strip():
            raise HTTPException(
                status_code=400, detail="Transcription failed or empty."
            )

        # 2. Process query & generate response conforming to Groq system prompt policy
        response_data = chat_service.generate_chat_response(transcription, lang)
        answer = response_data["response_text"]

        # 3. Text to Speech
        audio_base64 = ""
        try:
            tts_path = synthesize(answer)
            if os.path.exists(tts_path):
                with open(tts_path, "rb") as f:
                    audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                try:
                    os.unlink(tts_path)
                except Exception:
                    pass
        except Exception as tts_err:
            logger.exception(
                "Failed to synthesize TTS for audio chat: {}", tts_err
            )

        return {
            "transcription": response_data.get("cleaned_input", transcription),
            "answer": answer,
            "audio_base64": audio_base64,
        }
    except Exception as exc:
        logger.exception("Chat audio endpoint failed: {}", exc)
        raise HTTPException(status_code=500, detail=str(exc))
