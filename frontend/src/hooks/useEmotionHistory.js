import { useState, useCallback, useRef } from 'react';

const EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'];
const HISTORY_LENGTH = 15; // Number of frames to smooth over

export function useEmotionHistory() {
  const [history, setHistory] = useState([]);
  const [smoothedDistribution, setSmoothedDistribution] = useState(
    EMOTIONS.map(e => ({ name: e, confidence: 0 }))
  );
  const [currentSmoothedEmotion, setCurrentSmoothedEmotion] = useState(null);

  // We use a ref to track the latest history to avoid stale closures in fast updates
  const historyRef = useRef([]);

  const addPrediction = useCallback((predictions) => {
    if (!predictions || predictions.length === 0) return;

    // Create a dictionary of current confidences defaulting to 0
    const currentFrame = EMOTIONS.reduce((acc, curr) => {
      acc[curr] = 0;
      return acc;
    }, {});

    // For each prediction received, update the dictionary
    predictions.forEach(p => {
      if (currentFrame[p.emotion] !== undefined) {
        currentFrame[p.emotion] = p.confidence;
      }
    });

    // Add timestamp to frame
    currentFrame.timestamp = Date.now();
    // Add time short format for chart X-axis
    const date = new Date(currentFrame.timestamp);
    currentFrame.time = `${date.getSeconds()}.${date.getMilliseconds().toString().padStart(3, '0').substring(0,2)}`;

    // Update history
    const newHistory = [...historyRef.current, currentFrame].slice(-HISTORY_LENGTH);
    historyRef.current = newHistory;
    setHistory(newHistory);

    // Calculate averages
    const sums = EMOTIONS.reduce((acc, curr) => {
      acc[curr] = 0;
      return acc;
    }, {});

    newHistory.forEach(frame => {
      EMOTIONS.forEach(emotion => {
        sums[emotion] += frame[emotion];
      });
    });

    const averages = EMOTIONS.map(emotion => ({
      name: emotion,
      confidence: sums[emotion] / newHistory.length
    }));

    setSmoothedDistribution(averages);

    // Find the emotion with the highest smoothed confidence
    const topEmotion = averages.reduce((prev, current) => 
      (prev.confidence > current.confidence) ? prev : current
    );

    if (topEmotion.confidence > 0) {
       setCurrentSmoothedEmotion({
         emotion: topEmotion.name,
         confidence: topEmotion.confidence
       });
    }
  }, []);

  return { 
    addPrediction, 
    history, 
    smoothedDistribution, 
    currentSmoothedEmotion 
  };
}
