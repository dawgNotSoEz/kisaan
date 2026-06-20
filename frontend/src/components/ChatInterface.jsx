import React, { useState, useContext, useRef, useEffect } from 'react';
import { api } from '../services/api';
import { LanguageContext } from '../context/LanguageContext';
import { useVoice } from '../hooks/useVoice';

const TEXTS = {
  hi: {
    greeting: 'नमस्ते! मैं आपका किसान साथी हूँ। खेती से जुड़ा सवाल पूछें।',
    tapToSpeak: 'बोलने के लिए दबाएं (Tap to Record)',
    recording: 'रिकॉर्ड हो रहा है... रुकने के लिए दबाएं',
    stopAudio: 'ऑडियो रोकें',
    typeInstead: 'या टाइप करें...',
    send: 'भेजें',
    error: 'क्षमा करें, सर्वर से नहीं जुड़ पाया।',
    analyzing: 'आवाज़ समझ रहा हूँ...'
  },
  en: {
    greeting: 'Hello! I am Kisaan Saathi. Ask me farming questions.',
    tapToSpeak: 'Tap to Record',
    recording: 'Recording... Tap to Stop',
    stopAudio: 'Stop Audio',
    typeInstead: 'Or type here...',
    send: 'Send',
    error: 'Sorry, error connecting to server.',
    analyzing: 'Analyzing voice...'
  },
  ta: { greeting: 'வணக்கம்!', tapToSpeak: 'பேசவும்', recording: 'பதிவாகிறது...', stopAudio: 'நிறுத்து', typeInstead: 'தட்டச்சு செய்யவும்...', send: 'அனுப்பு', error: 'பிழை.', analyzing: 'செயலாக்குகிறது...' },
  te: { greeting: 'నమస్కారం!', tapToSpeak: 'మాట్లాడండి', recording: 'రికార్డ్ అవుతోంది...', stopAudio: 'ఆపు', typeInstead: 'టైప్ చేయండి...', send: 'పంపు', error: 'లోపం.', analyzing: 'విశ్లేషిస్తోంది...' },
  mr: { greeting: 'नमस्कार!', tapToSpeak: 'बोला', recording: 'रेकॉर्डिंग...', stopAudio: 'थांबवा', typeInstead: 'टाइप करा...', send: 'पाठवा', error: 'त्रुटी.', analyzing: 'आवाज समजून घेत आहे...' }
};

export default function ChatInterface() {
  const { lang } = useContext(LanguageContext);
  const t = TEXTS[lang] || TEXTS['hi'];
  
  const [messages, setMessages] = useState([{ role: 'ai', content: t.greeting }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isProcessingVoice, setIsProcessingVoice] = useState(false);
  
  const messagesEndRef = useRef(null);
  const { startRecording, stopRecording, isRecording, playAudioBase64, stopAudio, isPlaying } = useVoice();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (messages.length === 1) {
      setMessages([{ role: 'ai', content: t.greeting }]);
    }
    stopAudio();
  }, [lang, stopAudio, messages.length]);

  const handleTextSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userQuery }]);
    setLoading(true);
    stopAudio();

    try {
      const data = await api.chat(userQuery, lang);
      setMessages(prev => [...prev, { role: 'ai', content: data.answer }]);
      if (data.audio_base64) {
        playAudioBase64(data.audio_base64);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: t.error }]);
    } finally {
      setLoading(false);
    }
  };

  const toggleRecording = async () => {
    if (isRecording) {
      setIsProcessingVoice(true);
      const audioBlob = await stopRecording();
      if (audioBlob) {
        stopAudio();
        try {
          const data = await api.chatAudio(audioBlob, lang);
          // Show what the AI heard
          setMessages(prev => [...prev, { role: 'user', content: data.transcription }]);
          // Show the AI's answer
          setMessages(prev => [...prev, { role: 'ai', content: data.answer }]);
          
          if (data.audio_base64) {
            playAudioBase64(data.audio_base64);
          }
        } catch (err) {
          setMessages(prev => [...prev, { role: 'ai', content: t.error }]);
        } finally {
          setIsProcessingVoice(false);
        }
      } else {
        setIsProcessingVoice(false);
      }
    } else {
      stopAudio();
      startRecording();
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border-4 border-nature-100 flex flex-col h-[75vh]">
      
      {isPlaying && (
        <button onClick={stopAudio} className="bg-earth-500 hover:bg-earth-600 text-white p-3 font-bold text-center transition-all shadow-inner rounded-t-2xl">
          ⏸ {t.stopAudio}
        </button>
      )}

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-nature-50 rounded-t-2xl">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[90%] rounded-3xl p-4 shadow-md text-lg md:text-xl ${
              msg.role === 'user' 
                ? 'bg-nature-700 text-white rounded-br-none border-2 border-nature-800' 
                : 'bg-white border-2 border-nature-200 text-gray-900 rounded-bl-none font-medium'
            }`}>
              <p className="whitespace-pre-wrap break-words">{msg.content}</p>
            </div>
          </div>
        ))}
        {(loading || isProcessingVoice) && (
          <div className="flex justify-start">
             <div className="bg-white border-2 border-nature-200 rounded-3xl rounded-bl-none p-4 shadow-md flex gap-2 items-center text-nature-600 font-bold">
              {isProcessingVoice ? t.analyzing : "..."}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t-4 border-nature-100 rounded-b-3xl">
        <div className="flex flex-col items-center gap-3">
          
          <button
            type="button"
            onClick={toggleRecording}
            disabled={loading || isProcessingVoice}
            className={`flex flex-col items-center justify-center w-24 h-24 md:w-32 md:h-32 rounded-full shadow-xl transition-transform transform active:scale-95 disabled:opacity-50 ${
              isRecording 
                ? 'bg-red-500 text-white animate-pulse ring-4 ring-red-200 scale-105' 
                : 'bg-nature-600 text-white hover:bg-nature-500 ring-4 ring-nature-100'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 md:h-14 md:w-14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {isRecording ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              )}
            </svg>
            <span className="font-bold text-sm mt-1 text-center leading-tight px-2">{isRecording ? t.recording : t.tapToSpeak}</span>
          </button>

          <form onSubmit={handleTextSend} className="w-full flex items-center gap-2 mt-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t.typeInstead}
              className="flex-1 bg-gray-100 border-2 border-gray-300 rounded-2xl px-4 py-3 text-lg md:text-xl focus:outline-none focus:border-nature-600"
              disabled={loading || isRecording || isProcessingVoice}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading || isRecording || isProcessingVoice}
              className="px-6 py-3 bg-earth-500 text-white text-lg font-bold rounded-2xl hover:bg-earth-600 disabled:opacity-50"
            >
              {t.send}
            </button>
          </form>

        </div>
      </div>
    </div>
  );
}