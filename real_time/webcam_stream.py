"""
Optimized webcam stream with threading
"""

import cv2
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


class WebcamStream:
    """Threaded webcam capture for better performance"""
    
    def __init__(self, 
                 camera_id=config.WEBCAM_ID,
                 width=config.WEBCAM_WIDTH,
                 height=config.WEBCAM_HEIGHT,
                 fps=config.WEBCAM_FPS):
        """
        Initialize webcam stream
        
        Args:
            camera_id: Camera device ID
            width: Frame width
            height: Frame height
            fps: Target FPS
        """
        
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        
        # Initialize capture
        self.cap = cv2.VideoCapture(camera_id)
        
        if not self.cap.isOpened():
            raise ValueError(f"Could not open camera {camera_id}")
        
        # Set properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        
        # Get actual properties
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        print(f"Webcam initialized:")
        print(f"  Camera ID: {camera_id}")
        print(f"  Resolution: {actual_width}x{actual_height}")
        print(f"  FPS: {actual_fps}")
        
        # Threading
        self.frame = None
        self.grabbed = False
        self.stopped = False
        self.thread = None
    
    def start(self):
        """Start threaded capture"""
        if config.USE_THREADING:
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            print("Threaded webcam capture started")
        else:
            print("Non-threaded webcam capture mode")
        
        return self
    
    def _update(self):
        """Update frame in background thread"""
        while not self.stopped:
            self.grabbed, self.frame = self.cap.read()
            
            if not self.grabbed:
                self.stop()
                break
    
    def read(self):
        """
        Read current frame
        
        Returns:
            (grabbed, frame) tuple
        """
        if config.USE_THREADING:
            return self.grabbed, self.frame
        else:
            return self.cap.read()
    
    def stop(self):
        """Stop capture and release resources"""
        self.stopped = True
        
        if self.thread is not None:
            self.thread.join()
        
        if self.cap is not None:
            self.cap.release()
        
        print("Webcam stream stopped")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.stop()


if __name__ == '__main__':
    """Test webcam stream"""
    
    print("Testing webcam stream (press 'q' to quit)...")
    
    try:
        stream = WebcamStream()
        stream.start()
        
        while True:
            grabbed, frame = stream.read()
            
            if not grabbed or frame is None:
                print("Failed to grab frame")
                break
            
            cv2.imshow('Webcam Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        stream.stop()
        cv2.destroyAllWindows()
        
        print("\n✓ Webcam stream test completed!")
        
    except Exception as e:
        print(f"\n✗ Webcam test failed: {e}")
