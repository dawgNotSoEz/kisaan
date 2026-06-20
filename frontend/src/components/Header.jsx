import React, { useContext } from 'react';
import { LanguageContext } from '../context/LanguageContext';

export default function Header() {
  const { lang, setLang, LANGUAGES } = useContext(LanguageContext);

  return (
    <header className="bg-nature-700 text-white shadow-lg p-4 sticky top-0 z-50">
      <div className="max-w-4xl mx-auto flex justify-between items-center">
        <div className="flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-earth-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <h1 className="text-3xl font-extrabold tracking-tight">Kisaan Saathi</h1>
        </div>
        
        <select 
          value={lang}
          onChange={(e) => setLang(e.target.value)}
          className="bg-nature-800 border-2 border-nature-500 text-white text-lg font-bold p-2 px-4 rounded-xl cursor-pointer focus:outline-none focus:ring-4 focus:ring-earth-500 appearance-none text-center"
        >
          {LANGUAGES.map(l => (
            <option key={l.code} value={l.code}>{l.label}</option>
          ))}
        </select>
      </div>
    </header>
  );
}