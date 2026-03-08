import React, { useRef, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Camera, Video, VideoOff, ShieldCheck } from 'lucide-react';

const WebcamViewer = ({ onStreamChange }) => {
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [isActive, setIsActive] = useState(false);

  const startCamera = async () => {
    try {
      const newStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 1280, height: 720, facingMode: "user" } 
      });
      setStream(newStream);
      setIsActive(true);
      if (onStreamChange) onStreamChange(true);
    } catch (err) {
      console.error("Error accessing webcam:", err);
      alert("Could not access camera. Please check permissions.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsActive(false);
    if (onStreamChange) onStreamChange(false);
  };

  useEffect(() => {
    if (isActive && videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [isActive, stream]);

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="glass-card overflow-hidden flex flex-col h-full"
    >
      <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-white">
        <div className="flex items-center gap-2 font-semibold text-slate-700">
          <Video size={18} className="text-primary" />
          Live Feed
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-500 animate-pulse' : 'bg-slate-300'}`} />
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
            {isActive ? 'Active' : 'Offline'}
          </span>
        </div>
      </div>

      <div className="relative aspect-video bg-slate-900 flex items-center justify-center overflow-hidden">
        <AnimatePresence mode="wait">
          {!isActive ? (
            <motion.div 
              key="placeholder"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center text-slate-500"
            >
              <div className="bg-slate-800 p-6 rounded-full inline-block mb-4">
                <Camera size={48} className="text-slate-600" />
              </div>
              <p className="text-sm font-medium">Camera is currently disabled</p>
            </motion.div>
          ) : (
            <motion.div 
              key="video-container"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="w-full h-full relative"
            >
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover mirror"
              />
              <div className="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/60 to-transparent">
                <p className="text-white text-xs font-medium flex items-center gap-2">
                  <ShieldCheck size={14} className="text-green-400" />
                  Secure Local Processing
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="p-6 bg-white mt-auto flex gap-4">
        <button
          onClick={startCamera}
          disabled={isActive}
          className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold transition-all ${
            isActive 
              ? 'bg-slate-100 text-slate-400 cursor-not-allowed' 
              : 'bg-primary text-white hover:bg-indigo-700 shadow-lg shadow-indigo-100'
          }`}
        >
          <Video size={20} />
          Start Camera
        </button>
        <button
          onClick={stopCamera}
          disabled={!isActive}
          className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold transition-all ${
            !isActive 
              ? 'bg-slate-100 text-slate-400 cursor-not-allowed' 
              : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
          }`}
        >
          <VideoOff size={20} />
          Stop
        </button>
      </div>
    </motion.div>
  );
};

export default WebcamViewer;
