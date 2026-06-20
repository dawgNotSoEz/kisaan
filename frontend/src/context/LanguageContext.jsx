import React, { createContext, useState } from 'react';

export const LANGUAGES = [
  { code: 'hi', label: 'हिंदी', native: 'hi-IN' },
  { code: 'en', label: 'English', native: 'en-IN' },
  { code: 'ta', label: 'தமிழ்', native: 'ta-IN' },
  { code: 'te', label: 'తెలుగు', native: 'te-IN' },
  { code: 'mr', label: 'मराठी', native: 'mr-IN' }
];

export const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState('hi'); // Default to Hindi

  return (
    <LanguageContext.Provider value={{ lang, setLang, LANGUAGES }}>
      {children}
    </LanguageContext.Provider>
  );
};