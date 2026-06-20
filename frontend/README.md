# Kisaan Saathi (किसान साथी) - Frontend Client

**Kisaan Saathi** (Farmer's Companion) is a modern, responsive, and multilingual web application designed to support Indian farmers with agricultural assistance, AI-driven crop diagnosis, and real-time environmental insights.

The client is built on **React 19**, **Vite**, and styled with **Tailwind CSS**. It supports text/voice-based query handling and automated disease diagnosis, integrated with custom crop advisories.

---

## 🌟 Key Features

1. **AI Agricultural Assistant (Voice & Text)**
   - Allows users to speak or type farming questions in their native language.
   - Built-in audio recorder capturing audio chunks (`.webm`) and transmitting to the backend via binary multipart forms.
   - Plays AI voice responses directly via browser audio components.
2. **Interactive Crop Diagnosis Flow**
   - Step-by-step diagnostic wizard: **Crop** ➔ **Affected Part** ➔ **Visual Symptom / Observation**.
   - Retrieves organic/traditional management recommendations instantly.
3. **Live Weather & Soil Insights Dashboard (New)**
   - Custom integration with the **Open-Meteo Forecast API** for Delhi NCR (`latitude=28.61, longitude=77.20`).
   - Tracks real-time ambient parameters: Temperature, Humidity, and Precipitation.
   - Tracks subsurface variables: Soil Moisture ($0\text{ to }1\text{ cm}$) and Soil Temperature ($0\text{ cm}$).
   - Employs an intelligent local agricultural advisory that parses soil moisture data to suggest irrigation states.
   - Includes a mini-forecast showing trends for the next 5 hours.
4. **Multilingual Localizations**
   - Deep translation tables for 5 Indian languages: **Hindi (हिंदी)**, **English**, **Tamil (தமிழ்)**, **Telugu (తెలుగు)**, and **Marathi (मराठी)**.

---

## 📂 Project Architecture

```
kisaan-saathi-frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx           # Core Header with application title and language selector
│   │   ├── WeatherWidget.jsx    # Live weather, soil dashboard, agricultural advisory, and forecast
│   │   ├── ChatInterface.jsx    # Text & voice interface with playback control
│   │   └── DiagnosisFlow.jsx    # Step-by-step crop disease wizard
│   ├── context/
│   │   └── LanguageContext.jsx  # Context provider for multi-lingual translation state
│   ├── hooks/
│   │   └── useVoice.js          # Web Audio MediaRecorder hook for capturing and playing sound bytes
│   ├── services/
│   │   └── api.js               # Central service interface for backend & weather APIs
│   ├── App.jsx                  # Main wrapper coordinating view tabs and layout structure
│   ├── App.css                  # Custom styling utilities
│   ├── index.css                # Global imports, Tailwind v4 directives, and base configurations
│   └── main.jsx                 # Client entrypoint mounting react tree with provider wrappers
├── package.json                 # Project dependencies (React 19, Vite, Tailwind v4)
└── bun.lock                     # Lockfile for Bun package manager
```

### 🔗 Key Files Reference

- Main Application Controller: [App.jsx](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/App.jsx)
- Weather Insights Dashboard: [WeatherWidget.jsx](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/components/WeatherWidget.jsx)
- Voice & Chat Panel: [ChatInterface.jsx](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/components/ChatInterface.jsx)
- Diagnostic Tool: [DiagnosisFlow.jsx](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/components/DiagnosisFlow.jsx)
- API Services Layer: [api.js](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/services/api.js)
- Audio Utility Hook: [useVoice.js](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/hooks/useVoice.js)
- Global Theme Configurations: [tailwind.config.js](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/tailwind.config.js)

---

## ⚡ Weather & Soil API Integration Details

The app integrates live forecasts using the public Open-Meteo REST service:

- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Parameters**:
  - `latitude=28.61` & `longitude=77.20` (Research Station reference coordinates)
  - `hourly=soil_moisture_0_to_1cm,soil_temperature_0cm,temperature_2m,relative_humidity_2m,precipitation`

### 💡 Local Processing Logic

1. **Temporal Syncing**:
   Because the API returns a full array of hourly predictions, [WeatherWidget.jsx](file:///mnt/windows/Users/pkaur/Documents/Python/kisaan-saathi-frontend/src/components/WeatherWidget.jsx) calculates the absolute time difference (`Math.abs(tDate - now)`) to dynamically match the current index corresponding to the user's localized hour.
2. **Agricultural Advisories**:
   Based on the real-time soil moisture coefficient ($\text{m}^3/\text{m}^3$), the interface displays immediate tips:
   - **Dry Soil** ($< 0.15\text{ m}^3/\text{m}^3$): Irrigation is recommended.
   - **Wet/Saturated Soil** ($&gt; 0.35\text{ m}^3/\text{m}^3$): Avoid over-irrigation.
   - **Optimal Soil** ($0.15 \le \text{moisture} \le 0.35$): Soil conditions are excellent.

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have [Bun](https://bun.sh) (recommended) or Node.js installed.

### 1. Install Dependencies
```bash
bun install
# or
npm install
```

### 2. Start Local Development Server
```bash
bun run dev
# or
npm run dev
```
The app will run locally at `http://localhost:5173`.

### 3. Build for Production
To build static production files under the `dist/` directory:
```bash
bun run build
# or
npm run build
```

---

## 🔗 Backend Requirements

This client interacts with a local API backend server running at `http://localhost:8000`. Ensure the backend server is running and exposes the following routes:
- `GET /api/v1/crops?lang={lang}` - Fetch supported list of crops.
- `GET /api/v1/symptoms?crop_id={id}&lang={lang}` - Fetch parts & symptoms list.
- `GET /api/v1/remedy?crop_id={id}&part={part}&observation={obs}&lang={lang}` - Fetch remedy guide.
- `POST /api/v1/chat` - AI assistant text question handler.
- `POST /api/v1/chat/audio` - AI assistant voice handler (accepts voice recording file).
