import tempfile
from pathlib import Path

import streamlit as st

from src.logging.logger import logger
from src.models.request import FarmerRequest
from src.orchestrator.conversation_manager import ConversationManager
from src.voice.stt.transcriber import transcribe
from src.voice.tts.player import load_audio
from src.voice.tts.synthesizer import synthesize


st.set_page_config(
    page_title="KisanSaathi",
    page_icon="KS",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 44rem;
            padding: 1.25rem 1rem 2rem;
        }
        div[data-testid="stAudioInput"] {
            border: 1px solid #d7e3d3;
            border-radius: 8px;
            padding: 0.75rem;
            background: #fbfdf8;
        }
        .stButton > button {
            width: 100%;
            min-height: 2.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("KisanSaathi")
st.caption("Voice-first natural farming assistant")

st.info(
    "Phase 1 uses Streamlit's built-in audio recorder (`st.audio_input`) because it "
    "keeps recording state inside Streamlit and avoids the session instability often "
    "seen with WebRTC components."
)

logger.info("Audio capture started.")
recording = st.audio_input(
    "Record farmer voice",
    help="Tap to record, stop, then process the captured audio.",
)

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "response_audio" not in st.session_state:
    st.session_state.response_audio = b""
if "conversation_manager" not in st.session_state:
    st.session_state.conversation_manager = ConversationManager()
if "conversation_session_id" not in st.session_state:
    st.session_state.conversation_session_id = (
        st.session_state.conversation_manager.create_session()
    )
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if recording is not None:
    logger.info("Audio capture completed: {} bytes", recording.size)
    st.success("Voice recording captured.")
    st.audio(recording.getvalue(), format="audio/wav")

    if st.button("Process Voice", type="primary"):
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                audio_path = Path(temp_audio.name)
                temp_audio.write(recording.getbuffer())

            with st.status("Processing voice", expanded=True) as status:
                st.write("Transcribing speech...")
                transcript = transcribe(str(audio_path))
                st.session_state.transcript = transcript

                st.write("Routing farming query...")
                farmer_request = FarmerRequest(
                    session_id=st.session_state.conversation_session_id,
                    farmer_input=transcript,
                    detected_language="auto",
                    metadata={"source": "streamlit_voice"},
                )
                farmer_response = st.session_state.conversation_manager.process_request(
                    farmer_request
                )
                st.session_state.chat_history.append(
                    {
                        "request": farmer_request,
                        "response": farmer_response,
                    }
                )

                st.write("Generating spoken response...")
                tts_path = synthesize(farmer_response.response_text)
                st.session_state.response_audio = load_audio(tts_path)
                status.update(label="Voice response ready", state="complete")

        except Exception as exc:
            logger.exception("Voice pipeline failed.")
            st.error(f"Could not process the recording: {exc}")

if st.session_state.transcript:
    st.subheader("Transcript")
    st.text_area(
        "Recognized speech",
        value=st.session_state.transcript,
        height=140,
        disabled=True,
        label_visibility="collapsed",
    )

if st.session_state.chat_history:
    st.subheader("Conversation")
    for turn in st.session_state.chat_history:
        request = turn["request"]
        response = turn["response"]
        with st.chat_message("user"):
            st.write(request.farmer_input)
        with st.chat_message("assistant"):
            st.write(response.response_text)
            st.caption(
                f"Intent: {response.intent} | Confidence: {response.confidence:.2f} | "
                f"Source: {response.source}"
            )

if st.session_state.response_audio:
    st.subheader("Audio Response")
    st.audio(st.session_state.response_audio, format="audio/mp3")
else:
    st.warning("Record your voice to generate a spoken response.")
