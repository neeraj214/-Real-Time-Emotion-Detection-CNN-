"""
Real-time emotion detection engine
"""

import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from models.model_utils import load_model
from src.face_detection import create_face_detector, draw_face_bbox, extract_face_roi
from src.data_preprocessing import preprocess_face_for_inference
from utils.performance import FPSCounter, PerformanceProfiler


class EmotionDetector:
    """Real-time emotion detection system"""
    
    def __init__(self, 
                 model_path=None,
                 detector_type=None,
                 confidence_threshold=None):
        """
        Initialize emotion detector
        
        Args:
            model_path: Path to trained model
            detector_type: Face detector type ('haar' or 'mediapipe')
            confidence_threshold: Minimum confidence to display prediction
        """
        
        print("\n" + "=" * 70)
        print("INITIALIZING EMOTION DETECTOR")
        print("=" * 70)
        
        # Load model
        print("\nLoading emotion detection model...")
        if model_path is None:
            model_path = config.get_model_path()
        
        self.model = load_model(model_path=model_path)
        print(f"✓ Model loaded from: {model_path}")
        
        # Initialize face detector
        print("\nInitializing face detector...")
        if detector_type is None:
            detector_type = config.FACE_DETECTOR_TYPE
        
        self.face_detector = create_face_detector(detector_type)
        print(f"✓ Face detector initialized: {detector_type}")
        
        # Set confidence threshold
        if confidence_threshold is None:
            confidence_threshold = config.CONFIDENCE_THRESHOLD
        
        self.confidence_threshold = confidence_threshold
        
        # Performance monitoring
        self.fps_counter = FPSCounter()
        self.profiler = PerformanceProfiler()
        
        # Frame skip counter
        self.frame_count = 0
        self.frame_skip = config.FRAME_SKIP
        
        # Cache last predictions for skipped frames
        self.last_predictions = []
        
        print("\n" + "=" * 70)
        print("EMOTION DETECTOR READY")
        print("=" * 70)
        print(f"Confidence threshold: {self.confidence_threshold}")
        print(f"Frame skip: {self.frame_skip}")
        print("=" * 70 + "\n")
    
    def detect_emotions(self, frame, process_frame=True):
        """
        Detect emotions in a frame
        
        Args:
            frame: Input frame (BGR)
            process_frame: Whether to process this frame or use cached results
        
        Returns:
            Frame with emotion annotations, list of predictions
        """
        
        self.profiler.start('total')
        
        # Update FPS
        self.fps_counter.update()
        
        # Frame skipping logic
        self.frame_count += 1
        should_process = (self.frame_count % self.frame_skip == 0) or process_frame
        
        if should_process:
            # Detect faces
            self.profiler.start('face_detection')
            faces = self.face_detector.detect_faces(frame)
            self.profiler.end('face_detection')
            
            # Process each face
            predictions = []
            
            for bbox in faces:
                x, y, w, h = bbox
                
                # Extract face ROI
                face_roi = extract_face_roi(frame, bbox, padding=10)
                
                if face_roi.size == 0:
                    continue
                
                # Preprocess for inference
                self.profiler.start('preprocessing')
                face_input = preprocess_face_for_inference(face_roi)
                self.profiler.end('preprocessing')
                
                # Predict emotion
                self.profiler.start('inference')
                emotion_probs = self.model.predict(face_input, verbose=0)[0]
                self.profiler.end('inference')
                
                # Get top prediction
                emotion_id = np.argmax(emotion_probs)
                confidence = emotion_probs[emotion_id]
                emotion_label = config.EMOTION_LABELS[emotion_id]
                
                predictions.append({
                    'bbox': bbox,
                    'emotion': emotion_label,
                    'emotion_id': emotion_id,
                    'confidence': confidence,
                    'probabilities': emotion_probs
                })
            
            # Cache predictions
            self.last_predictions = predictions
        else:
            # Use cached predictions
            predictions = self.last_predictions
        
        # Draw annotations
        annotated_frame = self._draw_annotations(frame.copy(), predictions)
        
        self.profiler.end('total')
        
        return annotated_frame, predictions
    
    def _draw_annotations(self, frame, predictions):
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input frame
            predictions: List of prediction dictionaries
        
        Returns:
            Annotated frame
        """
        
        for pred in predictions:
            bbox = pred['bbox']
            emotion = pred['emotion']
            confidence = pred['confidence']
            
            # Only draw if confidence is above threshold
            if confidence >= self.confidence_threshold:
                # Choose color based on emotion
                color = self._get_emotion_color(pred['emotion_id'])
                
                # Draw bounding box and label
                draw_face_bbox(
                    frame,
                    bbox,
                    label=emotion,
                    confidence=confidence,
                    color=color
                )
        
        return frame
    
    def _get_emotion_color(self, emotion_id):
        """
        Get color for emotion
        
        Args:
            emotion_id: Emotion ID
        
        Returns:
            BGR color tuple
        """
        
        colors = {
            0: (0, 0, 255),      # Angry - Red
            1: (128, 0, 128),    # Disgust - Purple
            2: (255, 0, 255),    # Fear - Magenta
            3: (0, 255, 0),      # Happy - Green
            4: (255, 0, 0),      # Sad - Blue
            5: (0, 255, 255),    # Surprise - Yellow
            6: (255, 255, 255)   # Neutral - White
        }
        
        return colors.get(emotion_id, config.BBOX_COLOR)
    
    def get_fps(self):
        """Get current FPS"""
        return self.fps_counter.get_fps()
    
    def get_performance_stats(self):
        """Get performance statistics"""
        return {
            'fps': self.get_fps(),
            'face_detection': self.profiler.get_stats('face_detection'),
            'preprocessing': self.profiler.get_stats('preprocessing'),
            'inference': self.profiler.get_stats('inference'),
            'total': self.profiler.get_stats('total')
        }
    
    def print_performance_report(self):
        """Print performance report"""
        self.profiler.print_report()
        print(f"\nAverage FPS: {self.get_fps():.2f}")


if __name__ == '__main__':
    """Test emotion detector"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Test emotion detector')
    parser.add_argument('--model-path', type=str, default=None,
                        help='Path to trained model')
    parser.add_argument('--detector', type=str, default='haar',
                        choices=['haar', 'mediapipe'],
                        help='Face detector type')
    
    args = parser.parse_args()
    
    try:
        # Initialize detector
        detector = EmotionDetector(
            model_path=args.model_path,
            detector_type=args.detector
        )
        
        # Test on webcam
        print("Opening webcam (press 'q' to quit)...")
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect emotions
            annotated_frame, predictions = detector.detect_emotions(frame)
            
            # Draw FPS
            from utils.performance import draw_fps
            draw_fps(annotated_frame, detector.get_fps())
            
            # Display
            cv2.imshow('Emotion Detection Test', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Print performance report
        detector.print_performance_report()
        
        print("\n✓ Emotion detector test completed!")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease train the model first:")
        print("  python src/train.py")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
