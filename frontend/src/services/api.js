const BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? 'http://localhost:8000/api/v1' : 'https://kisaan-api.onrender.com/api/v1');


export const api = {
  getCrops: async (lang) => {
    const res = await fetch(`${BASE_URL}/crops?lang=${lang}`);
    if (!res.ok) throw new Error('Failed to fetch crops');
    return res.json();
  },

  getSymptoms: async (cropId, lang) => {
    const res = await fetch(`${BASE_URL}/symptoms?crop_id=${encodeURIComponent(cropId)}&lang=${lang}`);
    if (!res.ok) throw new Error('Failed to fetch symptoms');
    return res.json();
  },

  getRemedy: async (cropId, part, observation, lang) => {
    const res = await fetch(`${BASE_URL}/remedy?crop_id=${encodeURIComponent(cropId)}&part=${encodeURIComponent(part)}&observation=${encodeURIComponent(observation)}&lang=${lang}`);
    if (!res.ok) throw new Error('Failed to fetch remedy');
    return res.json();
  },

  chat: async (query, lang) => {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, lang })
    });
    if (!res.ok) throw new Error('Failed to communicate with AI');
    return res.json();
  },

  chatAudio: async (audioBlob, lang) => {
    const formData = new FormData();
    // The backend expects 'file' and 'lang'
    formData.append('file', audioBlob, 'audio.webm');
    formData.append('lang', lang);
    
    const res = await fetch(`${BASE_URL}/chat/audio`, {
      method: 'POST',
      body: formData
    });
    
    if (!res.ok) throw new Error('Failed to process audio with AI');
    return res.json();
  },

  getWeather: async () => {
    const url = 'https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&hourly=soil_moisture_0_to_1cm,soil_temperature_0cm,temperature_2m,relative_humidity_2m,precipitation';
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch weather data');
    return res.json();
  }
};