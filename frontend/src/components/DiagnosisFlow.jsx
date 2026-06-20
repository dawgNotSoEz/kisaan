import React, { useState, useEffect, useContext } from 'react';
import { api } from '../services/api';
import { LanguageContext } from '../context/LanguageContext';

const TEXTS = {
  hi: {
    title: 'बीमारी पहचानें (Diagnosis)',
    selectCrop: 'आपकी फसल कौन सी है?',
    selectPart: 'पौधे का कौन सा हिस्सा खराब है?',
    selectObs: 'क्या लक्षण दिख रहे हैं?',
    getRemedy: 'उपाय देखें',
    loading: 'खोजा जा रहा है...',
    reset: 'नया खोजें',
    backendError: '⚠️ बैकएंड सर्वर से कनेक्ट नहीं हो पा रहा है। क्या आपने http://localhost:8000 चालू किया है?',
    management: 'इलाज / प्रबंधन:'
  },
  en: {
    title: 'Crop Diagnosis',
    selectCrop: 'Select a Crop',
    selectPart: 'Affected Plant Part',
    selectObs: 'Visual Observation',
    getRemedy: 'Get Remedy',
    loading: 'Loading...',
    reset: 'Start Over',
    backendError: '⚠️ Cannot connect to backend server. Is it running on http://localhost:8000?',
    management: 'Management:'
  },
  ta: { title: 'Crop Diagnosis', selectCrop: 'பயிர் தேர்ந்தெடுக்கவும்', selectPart: 'பகுதி', selectObs: 'அறிகுறி', getRemedy: 'தீர்வு', loading: 'Loading...', reset: 'Reset', backendError: 'Backend not connected.', management: 'Management:' },
  te: { title: 'Crop Diagnosis', selectCrop: 'పంటను ఎంచుకోండి', selectPart: 'భాగం', selectObs: 'లక్షణం', getRemedy: 'పరిష్కారం', loading: 'Loading...', reset: 'Reset', backendError: 'Backend not connected.', management: 'Management:' },
  mr: { title: 'Crop Diagnosis', selectCrop: 'पीक निवडा', selectPart: 'भाग', selectObs: 'लक्षण', getRemedy: 'उपाय', loading: 'Loading...', reset: 'Reset', backendError: 'Backend not connected.', management: 'Management:' }
};

export default function DiagnosisFlow() {
  const { lang } = useContext(LanguageContext);
  const t = TEXTS[lang] || TEXTS['en'];
  
  const [crops, setCrops] = useState([]);
  const [symptomsData, setSymptomsData] = useState(null);
  const [remedy, setRemedy] = useState(null);
  
  const [selectedCrop, setSelectedCrop] = useState('');
  const [selectedPart, setSelectedPart] = useState('');
  const [selectedObservation, setSelectedObservation] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    const fetchCrops = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await api.getCrops(lang);
        if (isMounted) setCrops(data);
      } catch (err) {
        if (isMounted) setError(t.backendError);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchCrops();
    
    setSelectedCrop('');
    setSelectedPart('');
    setSelectedObservation('');
    setSymptomsData(null);
    setRemedy(null);
    
    return () => { isMounted = false; };
  }, [lang]);

  useEffect(() => {
    if (!selectedCrop) return;
    
    let isMounted = true;
    const fetchSymptoms = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await api.getSymptoms(selectedCrop, lang);
        if (isMounted) {
          setSymptomsData(data);
          setSelectedPart('');
          setSelectedObservation('');
        }
      } catch (err) {
        if (isMounted) setError(t.backendError);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchSymptoms();
    return () => { isMounted = false; };
  }, [selectedCrop, lang]);

  const handleGetRemedy = async () => {
    if (!selectedCrop || !selectedPart || !selectedObservation) return;
    try {
      setLoading(true);
      setError('');
      const data = await api.getRemedy(selectedCrop, selectedPart, selectedObservation, lang);
      setRemedy(data);
    } catch (err) {
      setError(t.backendError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border-4 border-nature-100 p-6 md:p-10">
      <h2 className="text-3xl font-extrabold text-nature-800 mb-8">{t.title}</h2>

      {error && (
        <div className="bg-red-100 text-red-800 p-6 rounded-2xl mb-8 text-xl font-bold border-2 border-red-300 shadow-sm">
          {error}
        </div>
      )}

      {!remedy ? (
        <div className="space-y-8">
          <div>
            <label className="block text-2xl font-bold text-gray-800 mb-3">{t.selectCrop}</label>
            <select 
              className="w-full border-4 border-nature-200 rounded-2xl shadow-inner bg-nature-50 p-5 text-2xl font-semibold text-nature-900 focus:border-nature-600 focus:outline-none"
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              disabled={loading || crops.length === 0}
            >
              <option value="">-- {t.selectCrop} --</option>
              {crops.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>

          {selectedCrop && (
            <div>
              <label className="block text-2xl font-bold text-gray-800 mb-3">{t.selectPart}</label>
              <select 
                className="w-full border-4 border-nature-200 rounded-2xl shadow-inner bg-nature-50 p-5 text-2xl font-semibold text-nature-900 focus:border-nature-600 focus:outline-none"
                value={selectedPart}
                onChange={(e) => {
                  setSelectedPart(e.target.value);
                  setSelectedObservation('');
                }}
                disabled={loading}
              >
                <option value="">-- {t.selectPart} --</option>
                {symptomsData?.parts?.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
              </select>
            </div>
          )}

          {selectedPart && (
            <div>
              <label className="block text-2xl font-bold text-gray-800 mb-3">{t.selectObs}</label>
              <select 
                className="w-full border-4 border-nature-200 rounded-2xl shadow-inner bg-nature-50 p-5 text-2xl font-semibold text-nature-900 focus:border-nature-600 focus:outline-none"
                value={selectedObservation}
                onChange={(e) => setSelectedObservation(e.target.value)}
                disabled={loading}
              >
                <option value="">-- {t.selectObs} --</option>
                {symptomsData?.observations?.map(obs => <option key={obs.id} value={obs.id}>{obs.name}</option>)}
              </select>
            </div>
          )}

          {selectedObservation && (
            <button
              onClick={handleGetRemedy}
              disabled={loading}
              className="w-full mt-6 bg-earth-500 hover:bg-earth-600 text-white font-extrabold text-3xl py-6 rounded-2xl shadow-xl transition-transform transform hover:scale-105 active:scale-95"
            >
              {loading ? t.loading : t.getRemedy}
            </button>
          )}
        </div>
      ) : (
        <div className="space-y-6">
          <div className="bg-nature-100 rounded-3xl p-8 border-4 border-nature-300 shadow-inner">
            <h3 className="text-4xl font-extrabold text-nature-900 mb-4">{remedy.disease_name}</h3>
            <div className="prose prose-xl max-w-none text-gray-800 mb-6 whitespace-pre-wrap font-medium leading-relaxed">
              <strong className="text-2xl text-nature-800 block mb-2">{t.management}</strong>
              {remedy.organic_management}
            </div>
          </div>
          <button
            onClick={() => setRemedy(null)}
            className="w-full border-4 border-gray-300 text-gray-800 bg-white hover:bg-gray-100 font-extrabold text-2xl py-5 rounded-2xl shadow-md transition-colors"
          >
            {t.reset}
          </button>
        </div>
      )}
    </div>
  );
}