"""
Configuration file for Real-Time Facial Emotion Detection System
Contains all hyperparameters, paths, and settings
"""

import os

# ============================================================================
# PROJECT PATHS
# ============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
SAVED_MODELS_DIR = os.path.join(MODEL_DIR, 'saved_models')

# ============================================================================
# EMOTION LABELS
# ============================================================================
# FER-2013 dataset emotion labels (0-6)
EMOTION_LABELS = {
    0: 'Angry',
    1: 'Disgust',
    2: 'Fear',
    3: 'Happy',
    4: 'Sad',
    5: 'Surprise',
    6: 'Neutral'
}

NUM_CLASSES = len(EMOTION_LABELS)

# ============================================================================
# DATA PARAMETERS
# ============================================================================
IMG_SIZE = 48  # FER-2013 images are 48x48
IMG_CHANNELS = 1  # Grayscale
INPUT_SHAPE = (IMG_SIZE, IMG_SIZE, IMG_CHANNELS)

# Data split ratios
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1

# ============================================================================
# MODEL ARCHITECTURE PARAMETERS
# ============================================================================
# Convolutional layers configuration
CONV_FILTERS = [32, 64, 128]  # Number of filters in each conv block
CONV_KERNEL_SIZE = (3, 3)
POOL_SIZE = (2, 2)

# Dense layers configuration
DENSE_UNITS = [256, 128]  # Units in each dense layer
DROPOUT_RATES = [0.5, 0.3]  # Dropout after each dense layer

# Batch Normalization
USE_BATCH_NORM = True

# ============================================================================
# TRAINING PARAMETERS
# ============================================================================
BATCH_SIZE = 64
EPOCHS = 50
LEARNING_RATE = 0.001
OPTIMIZER = 'adam'
LOSS = 'categorical_crossentropy'
METRICS = ['accuracy']

# Early stopping
EARLY_STOPPING_PATIENCE = 10
EARLY_STOPPING_MIN_DELTA = 0.001

# Learning rate reduction
LR_REDUCE_FACTOR = 0.5
LR_REDUCE_PATIENCE = 5
LR_MIN = 1e-7

# Model checkpoint
SAVE_BEST_ONLY = True
MONITOR_METRIC = 'val_accuracy'

# ============================================================================
# DATA AUGMENTATION PARAMETERS
# ============================================================================
AUGMENTATION_CONFIG = {
    'rotation_range': 15,
    'width_shift_range': 0.1,
    'height_shift_range': 0.1,
    'horizontal_flip': True,
    'zoom_range': 0.1,
    'shear_range': 0.1,
    'fill_mode': 'nearest'
}

# ============================================================================
# FACE DETECTION PARAMETERS
# ============================================================================
# Face detector type: 'haar' or 'mediapipe'
FACE_DETECTOR_TYPE = 'haar'

# Haar Cascade parameters
HAAR_CASCADE_PATH = 'haarcascade_frontalface_default.xml'
HAAR_SCALE_FACTOR = 1.1
HAAR_MIN_NEIGHBORS = 5
HAAR_MIN_SIZE = (30, 30)

# MediaPipe parameters
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.5
MEDIAPIPE_MODEL_SELECTION = 0  # 0 for short-range (2m), 1 for full-range (5m)

# ============================================================================
# REAL-TIME INFERENCE PARAMETERS
# ============================================================================
# Webcam settings
WEBCAM_ID = 0
WEBCAM_WIDTH = 640
WEBCAM_HEIGHT = 480
WEBCAM_FPS = 30

# Performance optimization
FRAME_SKIP = 2  # Process every Nth frame (1 = no skip, 2 = every other frame)
USE_THREADING = True  # Use threaded webcam capture

# Display settings
BBOX_COLOR = (0, 255, 0)  # Green bounding box
BBOX_THICKNESS = 2
TEXT_COLOR = (255, 255, 255)  # White text
TEXT_FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 0.7
TEXT_THICKNESS = 2
CONFIDENCE_THRESHOLD = 0.3  # Minimum confidence to display prediction

# FPS display
SHOW_FPS = True
FPS_POSITION = (10, 30)
FPS_COLOR = (0, 255, 255)  # Yellow

# ============================================================================
# MODEL OPTIMIZATION
# ============================================================================
# TensorFlow Lite conversion
ENABLE_TFLITE_CONVERSION = False
TFLITE_QUANTIZATION = False  # Post-training quantization

# ONNX conversion
ENABLE_ONNX_CONVERSION = False

# ============================================================================
# LOGGING AND VISUALIZATION
# ============================================================================
VERBOSE = 1  # Training verbosity (0, 1, or 2)
PLOT_TRAINING_HISTORY = True
SAVE_CONFUSION_MATRIX = True

# File names
MODEL_FILENAME = 'emotion_cnn_model.h5'
TFLITE_FILENAME = 'emotion_cnn_model.tflite'
ONNX_FILENAME = 'emotion_cnn_model.onnx'
TRAINING_HISTORY_FILENAME = 'training_history.csv'
CONFUSION_MATRIX_FILENAME = 'confusion_matrix.png'
TRAINING_PLOT_FILENAME = 'training_history.png'

# ============================================================================
# DATASET DOWNLOAD (FER-2013)
# ============================================================================
FER2013_CSV_FILENAME = 'fer2013.csv'
FER2013_KAGGLE_DATASET = 'msambare/fer2013'  # Kaggle dataset identifier

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_model_path(filename=MODEL_FILENAME):
    """Get full path to model file"""
    return os.path.join(SAVED_MODELS_DIR, filename)

def get_data_path(filename):
    """Get full path to data file"""
    return os.path.join(RAW_DATA_DIR, filename)

def ensure_dirs():
    """Create necessary directories if they don't exist"""
    dirs = [
        DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR,
        MODEL_DIR, SAVED_MODELS_DIR
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
