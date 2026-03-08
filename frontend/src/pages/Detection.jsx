import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Camera, Video, VideoOff, Activity, Smile, BarChart3, ShieldCheck } from 'lucide-react';

const Detection = () => {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState({ label: 'Neutral', confidence: 0, emoji: '😐', color: 'bg-slate-400' });

  // Mock emotion updates when camera is active
  useEffect(() => {
    let interval;
    if (isCameraActive) {
      const emotions = [
        { label: 'Happy', confidence: 92, emoji: '😊', color: 'bg-green-500' },
        { label: 'Surprise', confidence: 85, emoji: '😲', color: 'bg-yellow-500' },
        { label: 'Neutral', confidence: 98, emoji: '😐', color: 'bg-blue-500' },
        { label: 'Sad', confidence: 78, emoji: '😢', color: 'bg-indigo-500' },
      ];
      
      interval = setInterval(() => {
        const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
        setCurrentEmotion(randomEmotion);
      }, 3000);
    } else {
      setCurrentEmotion({ label: 'Waiting...', confidence: 0, emoji: '📷', color: 'bg-slate-300' });
    }
    return () => clearInterval(interval);
  }, [isCameraActive]);

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50 p-6 md:p-12">
      <div className="max-w-7xl mx-auto">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-10"
        >
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Real-Time Analysis</h1>
          <p className="text-slate-600">Connect your camera to start detecting facial expressions with AI.</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
          {/* Left: Webcam Preview Card */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card overflow-hidden flex flex-col"
          >
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-white">
              <div className="flex items-center gap-2 font-semibold text-slate-700">
                <Video size={18} className="text-primary" />
                Live Feed
              </div>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${isCameraActive ? 'bg-green-500 animate-pulse' : 'bg-slate-300'}`} />
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                  {isCameraActive ? 'Active' : 'Offline'}
                </span>
              </div>
            </div>

            <div className="relative aspect-video bg-slate-900 flex items-center justify-center overflow-hidden">
              <AnimatePresence mode="wait">
                {!isCameraActive ? (
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
                    key="video"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-indigo-500/10 to-transparent flex items-center justify-center"
                  >
                    <div className="text-white/20 animate-pulse">
                      <Activity size={120} />
                    </div>
                    {/* In a real app, a <video> or <img> element would go here */}
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
                onClick={() => setIsCameraActive(true)}
                disabled={isCameraActive}
                className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold transition-all ${
                  isCameraActive 
                    ? 'bg-slate-100 text-slate-400 cursor-not-allowed' 
                    : 'bg-primary text-white hover:bg-indigo-700 shadow-lg shadow-indigo-100'
                }`}
              >
                <Video size={20} />
                Start Camera
              </button>
              <button
                onClick={() => setIsCameraActive(false)}
                disabled={!isCameraActive}
                className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold transition-all ${
                  !isCameraActive 
                    ? 'bg-slate-100 text-slate-400 cursor-not-allowed' 
                    : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
                }`}
              >
                <VideoOff size={20} />
                Stop
              </button>
            </div>
          </motion.div>

          {/* Right: Emotion Panel */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col gap-6"
          >
            {/* Main Emotion Display */}
            <div className="glass-card p-8 bg-white flex-1">
              <div className="flex items-center gap-2 mb-8 text-slate-500 font-bold text-xs uppercase tracking-widest">
                <BarChart3 size={16} />
                Emotion Analytics
              </div>

              <div className="flex flex-col items-center justify-center py-10">
                <motion.div 
                  key={currentEmotion.label}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 200 }}
                  className="text-8xl mb-6"
                >
                  {currentEmotion.emoji}
                </motion.div>
                
                <motion.h2 
                  key={`${currentEmotion.label}-text`}
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  className="text-4xl font-black text-slate-900 mb-2"
                >
                  {currentEmotion.label}
                </motion.h2>

                <div className="w-full max-w-xs mt-8">
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-bold text-slate-500 uppercase">Confidence</span>
                    <span className="text-sm font-black text-primary">{currentEmotion.confidence}%</span>
                  </div>
                  <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
                    <motion.div 
                      key={currentEmotion.confidence}
                      initial={{ width: 0 }}
                      animate={{ width: `${currentEmotion.confidence}%` }}
                      transition={{ duration: 0.8, ease: "easeOut" }}
                      className={`h-full ${currentEmotion.color} rounded-full`}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Hint/Status Card */}
            <div className="glass-card p-6 bg-indigo-600 text-white flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-xl">
                <Activity size={24} />
              </div>
              <div>
                <p className="text-sm font-bold opacity-80 uppercase tracking-tighter">System Status</p>
                <p className="font-medium">Model loaded and ready for inference</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Detection;
