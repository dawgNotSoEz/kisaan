import React, { useState, useEffect, useContext } from 'react';
import { api } from '../services/api';
import { LanguageContext } from '../context/LanguageContext';

const TEXTS = {
  hi: {
    title: 'मौसम और मिट्टी की जानकारी',
    sub: 'नई दिल्ली क्षेत्र (लाइव डेटा)',
    temp: 'तापमान',
    humidity: 'हवा में नमी',
    rain: 'बारिश (वर्षा)',
    soilTemp: 'मिट्टी का तापमान',
    soilMoisture: 'मिट्टी की नमी',
    loading: 'मौसम की जानकारी लोड हो रही है...',
    error: 'मौसम डेटा प्राप्त करने में विफल।',
    advisory: 'कृषि सलाह:',
    drySoil: 'मिट्टी सूखी है। कृपया आवश्यकतानुसार सिंचाई करें।',
    wetSoil: 'मिट्टी में पर्याप्त नमी है। अभी पानी देने की आवश्यकता नहीं है।',
    optSoil: 'मिट्टी की स्थिति फसलों के लिए उत्तम है।',
    forecast: 'आगामी घंटों का पूर्वानुमान'
  },
  en: {
    title: 'Weather & Soil Insights',
    sub: 'New Delhi Area (Live Data)',
    temp: 'Temperature',
    humidity: 'Humidity',
    rain: 'Rain / Precip.',
    soilTemp: 'Soil Temp (Surface)',
    soilMoisture: 'Soil Moisture (0-1cm)',
    loading: 'Loading weather data...',
    error: 'Failed to fetch weather data.',
    advisory: 'Agri Advisory:',
    drySoil: 'Soil moisture is low. Irrigation is recommended.',
    wetSoil: 'Soil moisture is optimal/high. Avoid over-irrigation.',
    optSoil: 'Soil conditions are excellent for crop growth.',
    forecast: 'Hourly Forecast'
  },
  ta: {
    title: 'வானிலை மற்றும் மண் தகவல்',
    sub: 'புது தில்லி பகுதி (நேரடி தரவு)',
    temp: 'வெப்பநிலை',
    humidity: 'ஈரப்பதம்',
    rain: 'மழைப்பொழிவு',
    soilTemp: 'மண் வெப்பநிலை',
    soilMoisture: 'மண் ஈரப்பதம்',
    loading: 'வானிலை தரவு ஏற்றப்படுகிறது...',
    error: 'வானிலை தரவை பெற முடியவில்லை.',
    advisory: 'விவசாய ஆலோசனை:',
    drySoil: 'மண்ணின் ஈரப்பதம் குறைவாக உள்ளது. நீர் பாசனம் தேவை.',
    wetSoil: 'மண்ணின் ஈரப்பதம் அதிகமாக உள்ளது. அதிக தண்ணீர் பாய்ச்ச வேண்டாம்.',
    optSoil: 'மண் நிலை பயிர் வளர்ச்சிக்கு மிகவும் உகந்தது.',
    forecast: 'வருகிற மணிநேர முன்னறிவிப்பு'
  },
  te: {
    title: 'వాతావరణం & నేల అంతర్దృష్టులు',
    sub: 'న్యూఢిల్లీ ప్రాంతం (లైవ్ డేటా)',
    temp: 'ఉష్ణోగ్రత',
    humidity: 'తేమ',
    rain: 'వర్షపాతం',
    soilTemp: 'నేల ఉష్ణోగ్రత',
    soilMoisture: 'నేల తేమ',
    loading: 'వాతావరణ డేటా లోడ్ అవుతోంది...',
    error: 'వాతావరణ డేటాను పొందడంలో విఫలమైంది.',
    advisory: 'వ్యవసాయ సలహా:',
    drySoil: 'నేల తేమ తక్కువగా ఉంది. నీటి పారుదల సిఫార్సు చేయబడింది.',
    wetSoil: 'నేలలో తగినంత తేమ ఉంది. ఎక్కువ నీరు పోయకండి.',
    optSoil: 'నేల పరిస్థితులు పంట పెరుగుదలకు చాలా బాగున్నాయి.',
    forecast: 'గంటల సూచన'
  },
  mr: {
    title: 'हवामान आणि मातीची माहिती',
    sub: 'नवी दिल्ली क्षेत्र (थेट डेटा)',
    temp: 'तापमान',
    humidity: 'हवेतील दमटपणा',
    rain: 'पाऊस',
    soilTemp: 'मातीचे तापमान',
    soilMoisture: 'मातीतील ओलावा',
    loading: 'हवामान डेटा लोड होत आहे...',
    error: 'हवामान डेटा लोड करण्यात अयशस्वी.',
    advisory: 'कृषी सल्ला:',
    drySoil: 'माती कोरडी आहे. कृपया आवश्यकतेनुसार सिंचन करावे.',
    wetSoil: 'मातीत पुरेसा ओलावा आहे. जास्त सिंचन टाळावे.',
    optSoil: 'पिकांच्या वाढीसाठी मातीची स्थिती उत्कृष्ट आहे.',
    forecast: 'पुढील काही तासांचा अंदाज'
  }
};

export default function WeatherWidget() {
  const { lang } = useContext(LanguageContext);
  const t = TEXTS[lang] || TEXTS['en'];
  
  const [weatherData, setWeatherData] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    let isMounted = true;
    const fetchWeather = async () => {
      try {
        setLoading(true);
        setError(false);
        const data = await api.getWeather();
        if (isMounted) {
          setWeatherData(data);
          
          // Find index matching local hour
          const now = new Date();
          const hourlyTimes = data.hourly.time;
          let closestIndex = 0;
          let minDiff = Infinity;
          for (let i = 0; i < hourlyTimes.length; i++) {
            const tDate = new Date(hourlyTimes[i]);
            const diff = Math.abs(tDate - now);
            if (diff < minDiff) {
              minDiff = diff;
              closestIndex = i;
            }
          }
          setCurrentIndex(closestIndex);
        }
      } catch (err) {
        console.error(err);
        if (isMounted) setError(true);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchWeather();
    return () => { isMounted = false; };
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-3xl p-6 shadow-xl border-4 border-nature-100 flex items-center justify-center min-h-[200px]">
        <div className="flex flex-col items-center gap-3">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-nature-600"></div>
          <p className="text-xl font-bold text-gray-600">{t.loading}</p>
        </div>
      </div>
    );
  }

  if (error || !weatherData || currentIndex === null) {
    return (
      <div className="bg-red-50 rounded-3xl p-6 shadow-xl border-4 border-red-200 flex items-center justify-center min-h-[200px]">
        <p className="text-xl font-bold text-red-600">⚠️ {t.error}</p>
      </div>
    );
  }

  const currentHourData = {
    temp: weatherData.hourly.temperature_2m[currentIndex],
    humidity: weatherData.hourly.relative_humidity_2m[currentIndex],
    rain: weatherData.hourly.precipitation[currentIndex],
    soilTemp: weatherData.hourly.soil_temperature_0cm[currentIndex],
    soilMoisture: weatherData.hourly.soil_moisture_0_to_1cm[currentIndex],
  };

  const units = weatherData.hourly_units;

  // Determine advisory based on soil moisture
  let advisoryText = t.optSoil;
  let advisoryColor = 'bg-nature-100 border-nature-300 text-nature-800';
  if (currentHourData.soilMoisture < 0.15) {
    advisoryText = t.drySoil;
    advisoryColor = 'bg-amber-100 border-amber-300 text-amber-900';
  } else if (currentHourData.soilMoisture > 0.35) {
    advisoryText = t.wetSoil;
    advisoryColor = 'bg-blue-100 border-blue-300 text-blue-900';
  }

  // Get next 5 hours for quick forecast
  const forecastItems = [];
  for (let i = 1; i <= 5; i++) {
    const idx = currentIndex + i;
    if (idx < weatherData.hourly.time.length) {
      const timeStr = new Date(weatherData.hourly.time[idx]).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      forecastItems.push({
        time: timeStr,
        temp: weatherData.hourly.temperature_2m[idx],
        soilMoisture: weatherData.hourly.soil_moisture_0_to_1cm[idx],
        rain: weatherData.hourly.precipitation[idx],
      });
    }
  }

  return (
    <div className="bg-gradient-to-br from-white to-nature-50 rounded-3xl shadow-xl border-4 border-nature-100 p-6 md:p-8 flex flex-col gap-6 transition-all hover:shadow-2xl">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b-2 border-nature-100 pb-4 gap-2">
        <div>
          <h2 className="text-3xl font-extrabold text-nature-800 flex items-center gap-2">
            ⛅ {t.title}
          </h2>
          <p className="text-sm font-semibold text-gray-500">{t.sub}</p>
        </div>
        <div className="bg-nature-700 text-white font-extrabold px-4 py-2 rounded-2xl shadow-sm text-lg">
          {new Date().toLocaleDateString(lang === 'hi' ? 'hi-IN' : 'en-IN', { weekday: 'short', month: 'short', day: 'numeric' })}
        </div>
      </div>

      {/* Grid of Weather & Soil Params */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Temp */}
        <div className="bg-white p-4 rounded-2xl border-2 border-nature-100 shadow-sm flex flex-col items-center justify-center text-center hover:scale-105 transition-transform duration-200">
          <span className="text-4xl">🌡️</span>
          <span className="text-sm font-bold text-gray-500 mt-2">{t.temp}</span>
          <span className="text-2xl font-black text-nature-900 mt-1">{currentHourData.temp}{units.temperature_2m}</span>
        </div>

        {/* Humidity */}
        <div className="bg-white p-4 rounded-2xl border-2 border-nature-100 shadow-sm flex flex-col items-center justify-center text-center hover:scale-105 transition-transform duration-200">
          <span className="text-4xl">💧</span>
          <span className="text-sm font-bold text-gray-500 mt-2">{t.humidity}</span>
          <span className="text-2xl font-black text-nature-900 mt-1">{currentHourData.humidity}{units.relative_humidity_2m}</span>
        </div>

        {/* Precipitation */}
        <div className="bg-white p-4 rounded-2xl border-2 border-nature-100 shadow-sm flex flex-col items-center justify-center text-center hover:scale-105 transition-transform duration-200">
          <span className="text-4xl">🌧️</span>
          <span className="text-sm font-bold text-gray-500 mt-2">{t.rain}</span>
          <span className="text-2xl font-black text-nature-900 mt-1">{currentHourData.rain}{units.precipitation}</span>
        </div>

        {/* Soil Moisture */}
        <div className="bg-white p-4 rounded-2xl border-2 border-nature-100 shadow-sm flex flex-col items-center justify-center text-center hover:scale-105 transition-transform duration-200">
          <span className="text-4xl">🌱</span>
          <span className="text-sm font-bold text-gray-500 mt-2">{t.soilMoisture}</span>
          <span className="text-2xl font-black text-nature-900 mt-1">{currentHourData.soilMoisture} <span className="text-xs text-gray-500">m³/m³</span></span>
        </div>

        {/* Soil Temp */}
        <div className="bg-white p-4 rounded-2xl border-2 border-nature-100 shadow-sm flex flex-col items-center justify-center text-center col-span-2 lg:col-span-1 hover:scale-105 transition-transform duration-200">
          <span className="text-4xl">🌡️🟫</span>
          <span className="text-sm font-bold text-gray-500 mt-2">{t.soilTemp}</span>
          <span className="text-2xl font-black text-nature-900 mt-1">{currentHourData.soilTemp}{units.soil_temperature_0cm}</span>
        </div>
      </div>

      {/* Advisory Section */}
      <div className={`p-4 rounded-2xl border-2 shadow-sm font-bold text-lg md:text-xl flex gap-3 items-center ${advisoryColor}`}>
        <span className="text-2xl">💡</span>
        <div>
          <strong className="block text-sm uppercase tracking-wide opacity-80">{t.advisory}</strong>
          {advisoryText}
        </div>
      </div>

      {/* Mini Forecast */}
      <div className="border-t-2 border-nature-100 pt-4">
        <h3 className="text-lg font-bold text-nature-800 mb-3">{t.forecast}</h3>
        <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-thin">
          {forecastItems.map((item, idx) => (
            <div key={idx} className="bg-white p-3 rounded-xl border border-nature-100 shadow-inner flex flex-col items-center justify-center text-center min-w-[90px] flex-shrink-0">
              <span className="text-xs font-bold text-gray-400">{item.time}</span>
              <span className="text-base font-black text-gray-800 mt-1">{item.temp}°C</span>
              <span className="text-xs font-semibold text-gray-500 mt-1">🌱 {item.soilMoisture}</span>
              {item.rain > 0 && <span className="text-xs font-bold text-blue-500 mt-0.5">🌧️ {item.rain}mm</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
