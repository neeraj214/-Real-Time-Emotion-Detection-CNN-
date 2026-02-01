"""
Face detection utilities using Haar Cascade and MediaPipe
"""

import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


class FaceDetector:
    """Base class for face detectors"""
    
    def detect_faces(self, frame):
        """
        Detect faces in a frame
        
        Args:
            frame: Input image (BGR format)
        
        Returns:
            List of face bounding boxes [(x, y, w, h), ...]
        """
        raise NotImplementedError


class HaarCascadeDetector(FaceDetector):
    """Face detector using OpenCV Haar Cascade"""
    
    def __init__(self, 
                 cascade_path=None,
                 scale_factor=config.HAAR_SCALE_FACTOR,
                 min_neighbors=config.HAAR_MIN_NEIGHBORS,
                 min_size=config.HAAR_MIN_SIZE):
        """
        Initialize Haar Cascade face detector
        
        Args:
            cascade_path: Path to Haar Cascade XML file
            scale_factor: Scale factor for multi-scale detection
            min_neighbors: Minimum neighbors for detection
            min_size: Minimum face size (width, height)
        """
        
        if cascade_path is None:
            # Use OpenCV's built-in Haar Cascade
            cascade_path = cv2.data.haarcascades + config.HAAR_CASCADE_PATH
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise ValueError(f"Failed to load Haar Cascade from {cascade_path}")
        
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        
        print(f"Haar Cascade detector initialized")
        print(f"  Scale factor: {scale_factor}")
        print(f"  Min neighbors: {min_neighbors}")
        print(f"  Min size: {min_size}")
    
    def detect_faces(self, frame):
        """
        Detect faces using Haar Cascade
        
        Args:
            frame: Input image (BGR format)
        
        Returns:
            List of face bounding boxes [(x, y, w, h), ...]
        """
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces


class MediaPipeDetector(FaceDetector):
    """Face detector using MediaPipe"""
    
    def __init__(self,
                 min_detection_confidence=config.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
                 model_selection=config.MEDIAPIPE_MODEL_SELECTION):
        """
        Initialize MediaPipe face detector
        
        Args:
            min_detection_confidence: Minimum confidence for detection
            model_selection: 0 for short-range (2m), 1 for full-range (5m)
        """
        
        try:
            import mediapipe as mp
        except ImportError:
            raise ImportError(
                "MediaPipe not installed. Install with: pip install mediapipe"
            )
        
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=min_detection_confidence,
            model_selection=model_selection
        )
        
        print(f"MediaPipe detector initialized")
        print(f"  Min detection confidence: {min_detection_confidence}")
        print(f"  Model selection: {model_selection}")
    
    def detect_faces(self, frame):
        """
        Detect faces using MediaPipe
        
        Args:
            frame: Input image (BGR format)
        
        Returns:
            List of face bounding boxes [(x, y, w, h), ...]
        """
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            h, w = frame.shape[:2]
            
            for detection in results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                
                # Convert to absolute coordinates
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Ensure coordinates are within frame
                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)
                
                faces.append((x, y, width, height))
        
        return faces
    
    def __del__(self):
        """Clean up MediaPipe resources"""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()


def create_face_detector(detector_type=None):
    """
    Factory function to create face detector
    
    Args:
        detector_type: 'haar' or 'mediapipe'
    
    Returns:
        FaceDetector instance
    """
    
    if detector_type is None:
        detector_type = config.FACE_DETECTOR_TYPE
    
    detector_type = detector_type.lower()
    
    if detector_type == 'haar':
        return HaarCascadeDetector()
    elif detector_type == 'mediapipe':
        return MediaPipeDetector()
    else:
        raise ValueError(f"Unknown detector type: {detector_type}. Use 'haar' or 'mediapipe'")


def extract_face_roi(frame, bbox, padding=10):
    """
    Extract face region of interest from frame
    
    Args:
        frame: Input image
        bbox: Bounding box (x, y, w, h)
        padding: Padding around face in pixels
    
    Returns:
        Cropped face image
    """
    
    x, y, w, h = bbox
    
    # Add padding
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(frame.shape[1], x + w + padding)
    y2 = min(frame.shape[0], y + h + padding)
    
    # Extract ROI
    face_roi = frame[y1:y2, x1:x2]
    
    return face_roi


def draw_face_bbox(frame, bbox, label=None, confidence=None, 
                   color=config.BBOX_COLOR, thickness=config.BBOX_THICKNESS):
    """
    Draw bounding box and label on frame
    
    Args:
        frame: Input image
        bbox: Bounding box (x, y, w, h)
        label: Label text
        confidence: Confidence score
        color: Box color (B, G, R)
        thickness: Line thickness
    
    Returns:
        Frame with drawn bounding box
    """
    
    x, y, w, h = bbox
    
    # Draw rectangle
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
    
    # Draw label if provided
    if label is not None:
        text = label
        if confidence is not None:
            text = f"{label}: {confidence:.2f}"
        
        # Calculate text size for background
        (text_width, text_height), baseline = cv2.getTextSize(
            text, 
            config.TEXT_FONT, 
            config.TEXT_SCALE, 
            config.TEXT_THICKNESS
        )
        
        # Draw background rectangle for text
        cv2.rectangle(
            frame,
            (x, y - text_height - baseline - 5),
            (x + text_width, y),
            color,
            -1  # Filled
        )
        
        # Draw text
        cv2.putText(
            frame,
            text,
            (x, y - 5),
            config.TEXT_FONT,
            config.TEXT_SCALE,
            config.TEXT_COLOR,
            config.TEXT_THICKNESS,
            cv2.LINE_AA
        )
    
    return frame


if __name__ == '__main__':
    """Test face detection"""
    
    print("Testing face detection...")
    
    # Test Haar Cascade
    print("\n" + "=" * 70)
    print("Testing Haar Cascade Detector")
    print("=" * 70)
    
    try:
        haar_detector = create_face_detector('haar')
        print("✓ Haar Cascade detector created successfully")
    except Exception as e:
        print(f"✗ Error creating Haar Cascade detector: {e}")
    
    # Test MediaPipe
    print("\n" + "=" * 70)
    print("Testing MediaPipe Detector")
    print("=" * 70)
    
    try:
        mp_detector = create_face_detector('mediapipe')
        print("✓ MediaPipe detector created successfully")
    except Exception as e:
        print(f"✗ Error creating MediaPipe detector: {e}")
    
    # Test on webcam if available
    print("\n" + "=" * 70)
    print("Testing on webcam (press 'q' to quit)")
    print("=" * 70)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("⚠ Webcam not available")
    else:
        detector = create_face_detector()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces
            faces = detector.detect_faces(frame)
            
            # Draw bounding boxes
            for bbox in faces:
                draw_face_bbox(frame, bbox, label="Face")
            
            # Display
            cv2.putText(
                frame,
                f"Faces detected: {len(faces)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            cv2.imshow('Face Detection Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Webcam test completed")
