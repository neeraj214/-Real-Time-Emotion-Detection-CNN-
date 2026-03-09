import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BarChart3 } from 'lucide-react';

const EmotionPanel = ({ emotion }) => {
  const { label, confidence, emoji, color } = emotion;

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3 }}
      className="flex flex-col gap-6 h-full"
    >
      <div className="glass-card p-8 bg-white flex-1 flex flex-col">
        <div className="flex items-center gap-2 mb-8 text-slate-500 font-bold text-xs uppercase tracking-widest">
          <BarChart3 size={16} />
          Emotion Analytics
        </div>

        <div className="flex-1 flex flex-col items-center justify-center py-10">
          <AnimatePresence mode="wait">
            <motion.div 
              key={label}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              transition={{ type: "spring", stiffness: 200 }}
              className="text-8xl mb-6"
            >
              {emoji}
            </motion.div>
          </AnimatePresence>
          
          <AnimatePresence mode="wait">
            <motion.h2 
              key={`${label}-text`}
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -10, opacity: 0 }}
              className="text-4xl font-black text-slate-900 mb-2 text-center"
            >
              {label}
            </motion.h2>
          </AnimatePresence>

          <div className="w-full max-w-xs mt-8">
            <div className="flex justify-between mb-2">
              <span className="text-sm font-bold text-slate-500 uppercase">Confidence</span>
              <motion.span 
                key={confidence}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-sm font-black text-primary"
              >
                {confidence}%
              </motion.span>
            </div>
            <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
              <motion.div 
                key={confidence}
                initial={{ width: 0 }}
                animate={{ width: `${confidence}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className={`h-full ${color} rounded-full`}
              />
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default EmotionPanel;
