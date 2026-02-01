"""
Data preprocessing and loading utilities for FER-2013 dataset
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


def load_fer2013_data(csv_path=None):
    """
    Load FER-2013 dataset from CSV file
    
    Args:
        csv_path: Path to fer2013.csv file
    
    Returns:
        X: Image data as numpy array (N, 48, 48, 1)
        y: Labels as numpy array (N,)
    """
    
    if csv_path is None:
        csv_path = config.get_data_path(config.FER2013_CSV_FILENAME)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"FER-2013 dataset not found at {csv_path}\n"
            f"Please download it from Kaggle: https://www.kaggle.com/datasets/{config.FER2013_KAGGLE_DATASET}"
        )
    
    print(f"Loading FER-2013 dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"Total samples: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Extract pixels and labels
    pixels = df['pixels'].tolist()
    emotions = df['emotion'].values
    
    # Convert pixel strings to numpy arrays
    X = []
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.array(face).reshape(config.IMG_SIZE, config.IMG_SIZE)
        X.append(face)
    
    X = np.array(X, dtype='float32')
    y = np.array(emotions, dtype='int32')
    
    print(f"Data shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    print(f"Emotion distribution:")
    for emotion_id, emotion_name in config.EMOTION_LABELS.items():
        count = np.sum(y == emotion_id)
        percentage = (count / len(y)) * 100
        print(f"  {emotion_name:10s}: {count:5d} ({percentage:5.2f}%)")
    
    return X, y


def preprocess_data(X, y, normalize=True):
    """
    Preprocess image data
    
    Args:
        X: Image data (N, H, W)
        y: Labels (N,)
        normalize: Whether to normalize pixel values to [0, 1]
    
    Returns:
        X_processed: Preprocessed images (N, H, W, 1)
        y_processed: One-hot encoded labels (N, num_classes)
    """
    
    # Normalize pixel values
    if normalize:
        X = X / 255.0
    
    # Reshape to add channel dimension
    X = X.reshape(-1, config.IMG_SIZE, config.IMG_SIZE, config.IMG_CHANNELS)
    
    # One-hot encode labels
    y = to_categorical(y, num_classes=config.NUM_CLASSES)
    
    print(f"Preprocessed data shape: {X.shape}")
    print(f"Preprocessed labels shape: {y.shape}")
    
    return X, y


def split_data(X, y, train_ratio=None, val_ratio=None, test_ratio=None, random_state=42):
    """
    Split data into train, validation, and test sets
    
    Args:
        X: Image data
        y: Labels
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
        random_state: Random seed for reproducibility
    
    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """
    
    if train_ratio is None:
        train_ratio = config.TRAIN_RATIO
    if val_ratio is None:
        val_ratio = config.VAL_RATIO
    if test_ratio is None:
        test_ratio = config.TEST_RATIO
    
    # Ensure ratios sum to 1
    total = train_ratio + val_ratio + test_ratio
    if not np.isclose(total, 1.0):
        raise ValueError(f"Ratios must sum to 1.0, got {total}")
    
    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, 
        test_size=test_ratio, 
        random_state=random_state,
        stratify=y.argmax(axis=1) if len(y.shape) > 1 else y
    )
    
    # Second split: separate train and validation
    val_size = val_ratio / (train_ratio + val_ratio)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=val_size,
        random_state=random_state,
        stratify=y_temp.argmax(axis=1) if len(y_temp.shape) > 1 else y_temp
    )
    
    print(f"\nData split:")
    print(f"  Training:   {X_train.shape[0]:5d} samples ({train_ratio*100:.1f}%)")
    print(f"  Validation: {X_val.shape[0]:5d} samples ({val_ratio*100:.1f}%)")
    print(f"  Test:       {X_test.shape[0]:5d} samples ({test_ratio*100:.1f}%)")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def create_data_generator(augmentation_config=None):
    """
    Create ImageDataGenerator for data augmentation
    
    Args:
        augmentation_config: Dictionary of augmentation parameters
    
    Returns:
        ImageDataGenerator instance
    """
    
    if augmentation_config is None:
        augmentation_config = config.AUGMENTATION_CONFIG
    
    datagen = ImageDataGenerator(**augmentation_config)
    
    print("Data augmentation enabled with config:")
    for key, value in augmentation_config.items():
        print(f"  {key}: {value}")
    
    return datagen


def load_and_preprocess_fer2013(csv_path=None):
    """
    Complete pipeline: load, preprocess, and split FER-2013 data
    
    Args:
        csv_path: Path to fer2013.csv file
    
    Returns:
        Dictionary containing all data splits and generators
    """
    
    print("=" * 70)
    print("LOADING AND PREPROCESSING FER-2013 DATASET")
    print("=" * 70)
    
    # Load raw data
    X, y = load_fer2013_data(csv_path)
    
    # Preprocess
    X, y = preprocess_data(X, y)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)
    
    # Create data generator for training
    train_datagen = create_data_generator()
    
    # No augmentation for validation/test
    val_datagen = ImageDataGenerator()
    
    print("\n" + "=" * 70)
    print("DATA PREPROCESSING COMPLETE")
    print("=" * 70)
    
    return {
        'X_train': X_train,
        'X_val': X_val,
        'X_test': X_test,
        'y_train': y_train,
        'y_val': y_val,
        'y_test': y_test,
        'train_datagen': train_datagen,
        'val_datagen': val_datagen
    }


def preprocess_face_for_inference(face_img):
    """
    Preprocess a single face image for model inference
    
    Args:
        face_img: Face image as numpy array (H, W) or (H, W, C)
    
    Returns:
        Preprocessed image ready for model input (1, 48, 48, 1)
    """
    
    # Convert to grayscale if needed
    if len(face_img.shape) == 3:
        import cv2
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    
    # Resize to model input size
    import cv2
    face_img = cv2.resize(face_img, (config.IMG_SIZE, config.IMG_SIZE))
    
    # Normalize
    face_img = face_img.astype('float32') / 255.0
    
    # Reshape for model input
    face_img = face_img.reshape(1, config.IMG_SIZE, config.IMG_SIZE, config.IMG_CHANNELS)
    
    return face_img


if __name__ == '__main__':
    """Test data preprocessing"""
    
    print("Testing data preprocessing pipeline...")
    
    try:
        data = load_and_preprocess_fer2013()
        print("\n✓ Data preprocessing test successful!")
        
        # Test inference preprocessing
        test_face = np.random.randint(0, 255, (48, 48), dtype=np.uint8)
        processed = preprocess_face_for_inference(test_face)
        print(f"\n✓ Inference preprocessing test successful!")
        print(f"  Input shape: {test_face.shape}")
        print(f"  Output shape: {processed.shape}")
        
    except FileNotFoundError as e:
        print(f"\n⚠ {e}")
        print("\nTo download FER-2013:")
        print("1. Install Kaggle CLI: pip install kaggle")
        print("2. Set up Kaggle API credentials")
        print("3. Run: kaggle datasets download -d msambare/fer2013")
        print("4. Extract to data/raw/ directory")
