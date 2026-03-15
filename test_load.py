import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    print("Importing EmotionDetector...")
    from real_time.emotion_detector import EmotionDetector
    from config import config
    print("Initializing EmotionDetector...")
    detector = EmotionDetector()
    print("Detector initialized successfully!")
    print(f"Model path: {config.get_model_path()}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
