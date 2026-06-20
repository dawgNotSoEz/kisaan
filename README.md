# 🌱 KisanSaathi — Voice-First Multilingual Agricultural Assistant

KisanSaathi is a voice-first, AI-powered agricultural advisor designed to support farmers with instant, localized natural farming insights. Utilizing advanced Speech-to-Text (ASR), large language models (LLM), and Text-to-Speech (TTS) pipelines, KisanSaathi understands multilingual requests (Hindi, English, Hinglish) and provides direct, actionable organic farming advice and disease remedies.

---

## 🚀 Key Features

*   🎙️ **Voice-First Interaction:** Speech-to-Text and Text-to-Speech translation pipeline for fluid, natural spoken conversations.
*   🇮🇳 **Multilingual Support:** Seamlessly detects and responds in Hindi (Devanagari script), English, and Hinglish.
*   🌾 **Disease Diagnosis Flow:** Interactive selector for crops, plant parts, and observations to provide targeted, organic remedy advisories.
*   🤖 **AI Agricultural Expert:** Integrated with Groq LLM (`llama-3.3-70b-versatile`) with prompt guardrails to guarantee strictly agricultural guidance.
*   ⚡ **Modern Stack:** Built using FastAPI (Backend) and React + Vite + Tailwind CSS (Frontend).

---

## 🛠️ Technology Stack

### Backend
*   **Core Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
*   **AI Inference:** [Groq Cloud SDK](https://wow.groq.com/) (Llama-3.3-70b)
*   **Speech Services:** 
    *   *STT:* Groq Whisper API
    *   *TTS:* gTTS (Google Text-to-Speech)
*   **Environment Management:** `uv` & Python Virtual Environment

### Frontend
*   **Core Library:** React 19 + Vite
*   **Styling:** Tailwind CSS (PostCSS)
*   **Execution Runtime:** Bun / Node.js

---

## 📂 Project Structure

```text
kisaan-saathi/
├── backend/               # FastAPI python backend
│   ├── src/
│   │   ├── llm/           # LLM config and factory
│   │   ├── orchestrator/  # Intent router & conversation manager
│   │   ├── services/      # Chat and disease database service
│   │   └── voice/         # STT transcriber & TTS synthesizer
│   ├── app.py             # Streamlit web app interface (Phase 1)
│   ├── main.py            # FastAPI main entrypoint (Phase 2)
│   └── requirements.txt   # Python dependencies
│
└── frontend/              # React single page application
    ├── src/
    │   ├── components/    # ChatInterface, Weather, and DiagnosisFlow
    │   ├── services/      # API communication layer
    │   └── App.jsx        # Main application layout
    ├── package.json       # Node dependency definition
    └── index.html         # Application root HTML
```

---

## ⚡ Quick Start

### 1. Backend Setup

Ensure you have Python 3.11+ installed. Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment and install dependencies:
```bash
# Create virtual environment using uv (recommended for speed)
uv venv .venv --python 3.11

# Install packages
uv pip install -r requirements.txt
uv pip install fastapi
```

Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

Start the FastAPI server:
```bash
$env:PYTHONUTF8=1; .venv\Scripts\python.exe -u -m uvicorn main:app --host 127.0.0.1 --port 8000
```
The backend API will be available at `http://127.0.0.1:8000`.

### 2. Frontend Setup

Ensure you have Bun or Node.js installed. Navigate to the frontend directory:

```bash
cd ../frontend
```

Install packages:
```bash
bun install
# or
npm install
```

Start the development server:
```bash
bun dev
# or
npm run dev
```
The application will open at `http://localhost:5173` (or `5174`).

---

## 🩺 Disease Advisory Database

KisanSaathi includes direct organic diagnosis and remedies for several common regional crop issues:
*   **Tomato (टमाटर):** Early Blight ( spots on leaves), Yellowing (deficiency/mosaic virus), Blossom End Rot (fruit rot).
*   **Wheat (गेहूं):** Nitrogen Deficiency, Rust Disease.
*   **Potato (आलू):** Late Blight, Tuber Soft Rot.
*   **Chilli (मिर्च):** Leaf Curl Virus.
*   **Paddy (धान):** Rice Blast.

---

## 📄 License
This project is open-source and available under the MIT License.
