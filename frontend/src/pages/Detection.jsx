import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Smile, BarChart3 } from 'lucide-react';
import WebcamViewer from '../components/WebcamViewer';

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
          {/* Left: Webcam Viewer component */}
          <WebcamViewer onStreamChange={setIsCameraActive} />

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
