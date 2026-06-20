import React, { useState, useContext } from 'react';
import Header from './components/Header';
import DiagnosisFlow from './components/DiagnosisFlow';
import ChatInterface from './components/ChatInterface';
import WeatherWidget from './components/WeatherWidget';
import { LanguageContext } from './context/LanguageContext';

function App() {
  const { lang } = useContext(LanguageContext);
  const [activeTab, setActiveTab] = useState('chat');

  const t = {
    hi: { chatTab: '🎤 बोलकर पूछें', diagTab: '🔍 बीमारी पहचानें' },
    en: { chatTab: '🎤 Ask via Voice', diagTab: '🔍 Identify Disease' },
    ta: { chatTab: '🎤 கேளுங்கள்', diagTab: '🔍 நோய் கண்டறிதல்' },
    te: { chatTab: '🎤 అడగండి', diagTab: '🔍 వ్యాధి గుర్తింపు' },
    mr: { chatTab: '🎤 विचार', diagTab: '🔍 रोग ओळख' }
  };
  
  const text = t[lang] || t['hi'];

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col font-sans">
      <Header />
      
      <main className="flex-1 max-w-5xl w-full mx-auto p-4 md:p-8 flex flex-col gap-8">
        
        {/* Weather & Soil Insights widget */}
        <WeatherWidget />

        {/* Massive Toggle Buttons */}
        <div className="flex bg-gray-300 p-2 rounded-3xl w-full mx-auto shadow-inner">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex-1 py-4 px-6 rounded-2xl font-extrabold text-xl md:text-2xl transition-all ${
              activeTab === 'chat' 
                ? 'bg-white text-nature-800 shadow-lg transform scale-105' 
                : 'text-gray-700 hover:bg-gray-200 hover:scale-100'
            }`}
          >
            {text.chatTab}
          </button>
          <button
            onClick={() => setActiveTab('diagnosis')}
            className={`flex-1 py-4 px-6 rounded-2xl font-extrabold text-xl md:text-2xl transition-all ${
              activeTab === 'diagnosis' 
                ? 'bg-white text-nature-800 shadow-lg transform scale-105' 
                : 'text-gray-700 hover:bg-gray-200 hover:scale-100'
            }`}
          >
            {text.diagTab}
          </button>
        </div>

        {/* View */}
        <div className="w-full">
          {activeTab === 'chat' ? <ChatInterface /> : <DiagnosisFlow />}
        </div>
      </main>
    </div>
  );
}

export default App;