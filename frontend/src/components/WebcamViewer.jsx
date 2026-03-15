import React, { useRef, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Camera, Video, VideoOff, ShieldCheck } from 'lucide-react';

const WebcamViewer = ({ onStreamChange, onEmotionResults }) => {
  const [stream, setStream] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const videoRef = useRef(null);
  const wsRef = useRef(null);
  const canvasRef = useRef(null);
  const requestRef = useRef(null);

  // Use a callback ref to ensure we set srcObject as soon as the element mounts
  const setVideoRef = (node) => {
    videoRef.current = node;
    if (node && stream) {
      node.srcObject = stream;
    }
  };

  // Initialize canvas for frame capturing
  useEffect(() => {
    canvasRef.current = document.createElement('canvas');
  }, []);

  const startCamera = async () => {
    try {
      const newStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480, facingMode: "user" }
      });
      setStream(newStream);
      setIsActive(true);
      if (onStreamChange) onStreamChange(true);
      
      // Initialize WebSocket
      connectWebSocket();
    } catch (err) {
      console.error("Error accessing webcam:", err);
      alert("Could not access camera. Please check permissions.");
    }
  };

  const connectWebSocket = () => {
    // Force localhost:8000 for now to avoid hostname issues
    const wsUrl = `ws://localhost:8000/ws/detect`;
    console.log("Connecting to WebSocket:", wsUrl);
    
    wsRef.current = new WebSocket(wsUrl);
    
    wsRef.current.onopen = () => {
      console.log("WebSocket connected successfully");
      startInferenceLoop();
    };
    
    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (onEmotionResults && data.predictions) {
          onEmotionResults(data.predictions);
        }
      } catch (e) {
        console.error("Error parsing WebSocket message:", e);
      }
    };
    
    wsRef.current.onclose = (event) => {
      console.log("WebSocket connection closed:", event.code, event.reason);
      stopInferenceLoop();
    };
    
    wsRef.current.onerror = (err) => {
      console.error("WebSocket error details:", err);
    };
  };

  const isActiveRef = useRef(false);

  useEffect(() => {
    isActiveRef.current = isActive;
  }, [isActive]);

  const startInferenceLoop = () => {
    console.log("DEBUG: Starting inference loop");
    if (requestRef.current) clearInterval(requestRef.current);
    
    requestRef.current = setInterval(() => {
      const currentIsActive = isActiveRef.current;
      const wsOpen = wsRef.current && wsRef.current.readyState === WebSocket.OPEN;
      
      if (!currentIsActive || !videoRef.current || !wsOpen) {
        return;
      }

      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      if (video.videoWidth > 0 && video.videoHeight > 0) {
        // Capture frame at optimized resolution for model inference
        canvas.width = 320; 
        canvas.height = 240;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        try {
          const base64Image = canvas.toDataURL('image/jpeg', 0.7);
          wsRef.current.send(JSON.stringify({ image: base64Image }));
        } catch (err) {
          console.error("Failed to send frame:", err);
        }
      }
    }, 200);
  };

  const stopInferenceLoop = () => {
    console.log("DEBUG: Stopping inference loop");
    if (requestRef.current) {
      clearInterval(requestRef.current);
      requestRef.current = null;
    }
  };

  const stopCamera = () => {
    stopInferenceLoop();
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    
    setIsActive(false);
    if (onStreamChange) onStreamChange(false);
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

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
                ref={setVideoRef}
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
