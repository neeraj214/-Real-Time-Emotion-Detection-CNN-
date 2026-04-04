import React, { useState, useCallback, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Activity } from 'lucide-react';
import WebcamViewer from '../components/WebcamViewer';
import EmotionPanel from '../components/EmotionPanel';
import { useEmotionHistory } from '../hooks/useEmotionHistory';
import AnalyticsDashboard from '../components/AnalyticsDashboard';

const EMOTION_MAP = {
  'Angry': { emoji: '😠', color: 'bg-red-500' },
  'Disgust': { emoji: '🤢', color: 'bg-purple-600' },
  'Fear': { emoji: '😨', color: 'bg-orange-500' },
  'Happy': { emoji: '😊', color: 'bg-green-500' },
  'Sad': { emoji: '😢', color: 'bg-blue-600' },
  'Surprise': { emoji: '😲', color: 'bg-yellow-500' },
  'Neutral': { emoji: '😐', color: 'bg-slate-400' }
};

const Detection = () => {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const { addPrediction, history, smoothedDistribution, currentSmoothedEmotion } = useEmotionHistory();

  const handleEmotionResults = useCallback((predictions) => {
    addPrediction(predictions);
  }, [addPrediction]);

  const displayEmotion = useMemo(() => {
    if (!currentSmoothedEmotion) {
      return { 
        label: 'Waiting...', 
        confidence: 0, 
        emoji: '📷', 
        color: 'bg-slate-300' 
      };
    }
    
    const { emotion, confidence } = currentSmoothedEmotion;
    const mapInfo = EMOTION_MAP[emotion] || { emoji: '❓', color: 'bg-slate-400' };
    
    return {
      label: emotion,
      confidence: Math.round(confidence * 100),
      emoji: mapInfo.emoji,
      color: mapInfo.color
    };
  }, [currentSmoothedEmotion]);

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
          <div>
            <WebcamViewer 
              onStreamChange={setIsCameraActive} 
              onEmotionResults={handleEmotionResults}
            />
          </div>

          {/* Right: Emotion Panel component and Dashboard */}
          <div className="flex flex-col gap-6">
            <EmotionPanel emotion={displayEmotion} />
            
            {/* Hint/Status Card */}
            <div className="glass-card p-6 bg-indigo-600 text-white flex items-center gap-4 rounded-2xl shadow-sm">
              <div className="bg-white/20 p-3 rounded-xl">
                <Activity size={24} />
              </div>
              <div>
                <p className="text-sm font-bold opacity-80 uppercase tracking-tighter">System Status</p>
                <p className="font-medium">
                  {isCameraActive ? 'Processing live frames...' : 'Model loaded and ready for inference'}
                </p>
              </div>
            </div>

            {/* Real-Time Analytics Dashboard */}
            <AnalyticsDashboard 
              history={history} 
              smoothedDistribution={smoothedDistribution} 
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Detection;
