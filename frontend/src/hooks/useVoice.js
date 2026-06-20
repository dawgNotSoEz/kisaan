import { useState, useRef, useCallback } from 'react';

export const useVoice = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const currentAudioRef = useRef(null);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Mic error:", err);
      alert("Microphone permission denied or not supported on this device.");
    }
  }, []);

  const stopRecording = useCallback(() => {
    return new Promise((resolve) => {
      if (!mediaRecorderRef.current) return resolve(null);
      
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setIsRecording(false);
        // Stop all mic tracks to release the hardware light
        mediaRecorderRef.current.stream.getTracks().forEach(t => t.stop());
        resolve(audioBlob);
      };
      
      mediaRecorderRef.current.stop();
    });
  }, []);

  const playAudioBase64 = useCallback((base64String) => {
    if (!base64String) return;
    
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
    }
    
    const snd = new Audio("data:audio/mp3;base64," + base64String);
    currentAudioRef.current = snd;
    
    snd.onplay = () => setIsPlaying(true);
    snd.onended = () => setIsPlaying(false);
    snd.onerror = (e) => {
      console.error("Audio playback error:", e);
      setIsPlaying(false);
    };
    
    snd.play().catch(e => {
      console.error("Failed to play audio:", e);
      setIsPlaying(false);
    });
  }, []);

  const stopAudio = useCallback(() => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      setIsPlaying(false);
    }
  }, []);

  return { startRecording, stopRecording, isRecording, playAudioBase64, stopAudio, isPlaying };
};