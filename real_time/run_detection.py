"""
Real-time emotion detection - Main entry point
Run this script to start real-time emotion detection from webcam
"""

import cv2
import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from real_time.webcam_stream import WebcamStream
from real_time.emotion_detector import EmotionDetector
from utils.performance import draw_fps


def main():
    """Main function for real-time emotion detection"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Real-Time Facial Emotion Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python real_time/run_detection.py
  python real_time/run_detection.py --detector mediapipe
  python real_time/run_detection.py --model-path models/saved_models/my_model.h5
  python real_time/run_detection.py --frame-skip 1 --no-threading

Controls:
  q - Quit
  s - Save screenshot
  p - Print performance report
  r - Reset performance counters
        """
    )
    
    parser.add_argument(
        '--model-path',
        type=str,
        default=None,
        help='Path to trained model (default: models/saved_models/emotion_cnn_model.h5)'
    )
    
    parser.add_argument(
        '--detector',
        type=str,
        default=config.FACE_DETECTOR_TYPE,
        choices=['haar', 'mediapipe'],
        help=f'Face detector type (default: {config.FACE_DETECTOR_TYPE})'
    )
    
    parser.add_argument(
        '--camera-id',
        type=int,
        default=config.WEBCAM_ID,
        help=f'Camera device ID (default: {config.WEBCAM_ID})'
    )
    
    parser.add_argument(
        '--frame-skip',
        type=int,
        default=config.FRAME_SKIP,
        help=f'Process every Nth frame (default: {config.FRAME_SKIP})'
    )
    
    parser.add_argument(
        '--confidence',
        type=float,
        default=config.CONFIDENCE_THRESHOLD,
        help=f'Minimum confidence threshold (default: {config.CONFIDENCE_THRESHOLD})'
    )
    
    parser.add_argument(
        '--no-threading',
        action='store_true',
        help='Disable threaded webcam capture'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=config.WEBCAM_WIDTH,
        help=f'Webcam width (default: {config.WEBCAM_WIDTH})'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=config.WEBCAM_HEIGHT,
        help=f'Webcam height (default: {config.WEBCAM_HEIGHT})'
    )
    
    args = parser.parse_args()
    
    # Override config if needed
    if args.no_threading:
        config.USE_THREADING = False
    
    config.FRAME_SKIP = args.frame_skip
    
    print("\n" + "=" * 70)
    print("REAL-TIME FACIAL EMOTION DETECTION")
    print("=" * 70)
    print("\nStarting system...")
    
    try:
        # Initialize emotion detector
        detector = EmotionDetector(
            model_path=args.model_path,
            detector_type=args.detector,
            confidence_threshold=args.confidence
        )
        
        # Initialize webcam
        print("\nInitializing webcam...")
        stream = WebcamStream(
            camera_id=args.camera_id,
            width=args.width,
            height=args.height
        )
        stream.start()
        
        print("\n" + "=" * 70)
        print("SYSTEM READY")
        print("=" * 70)
        print("\nControls:")
        print("  q - Quit")
        print("  s - Save screenshot")
        print("  p - Print performance report")
        print("  r - Reset performance counters")
        print("=" * 70 + "\n")
        
        screenshot_count = 0
        
        # Main loop
        while True:
            # Read frame
            grabbed, frame = stream.read()
            
            if not grabbed or frame is None:
                print("Failed to grab frame")
                break
            
            # Detect emotions
            annotated_frame, predictions = detector.detect_emotions(frame)
            
            # Draw FPS
            if config.SHOW_FPS:
                draw_fps(annotated_frame, detector.get_fps())
            
            # Draw info
            info_text = f"Faces: {len(predictions)} | Frame skip: {args.frame_skip}"
            cv2.putText(
                annotated_frame,
                info_text,
                (10, annotated_frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )
            
            # Display
            cv2.imshow('Real-Time Emotion Detection', annotated_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            
            elif key == ord('s'):
                screenshot_count += 1
                filename = f'screenshot_{screenshot_count}.png'
                cv2.imwrite(filename, annotated_frame)
                print(f"Screenshot saved: {filename}")
            
            elif key == ord('p'):
                print("\n" + "=" * 70)
                detector.print_performance_report()
                print("=" * 70)
            
            elif key == ord('r'):
                detector.fps_counter.reset()
                detector.profiler.reset()
                print("Performance counters reset")
        
        # Cleanup
        stream.stop()
        cv2.destroyAllWindows()
        
        # Final performance report
        print("\n" + "=" * 70)
        print("FINAL PERFORMANCE REPORT")
        print("=" * 70)
        detector.print_performance_report()
        
        print("\n" + "=" * 70)
        print("SYSTEM SHUTDOWN COMPLETE")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print("\n" + "=" * 70)
        print("ERROR: Model not found")
        print("=" * 70)
        print(f"\n{e}")
        print("\nPlease train the model first:")
        print("  1. Download FER-2013 dataset")
        print("  2. Run: python src/train.py")
        print("  3. Then run this script again")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("ERROR")
        print("=" * 70)
        print(f"\n{e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
