"""
Model utility functions for saving, loading, and converting models
"""

import os
import tensorflow as tf
from tensorflow import keras
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


def save_model(model, filename=None, save_dir=None):
    """
    Save trained model to disk
    
    Args:
        model: Keras model to save
        filename: Name of the file (default from config)
        save_dir: Directory to save to (default from config)
    
    Returns:
        Path to saved model
    """
    
    if filename is None:
        filename = config.MODEL_FILENAME
    
    if save_dir is None:
        save_dir = config.SAVED_MODELS_DIR
    
    os.makedirs(save_dir, exist_ok=True)
    
    model_path = os.path.join(save_dir, filename)
    model.save(model_path)
    
    print(f"Model saved to: {model_path}")
    return model_path


def load_model(filename=None, model_path=None):
    """
    Load trained model from disk
    
    Args:
        filename: Name of the model file
        model_path: Full path to model (overrides filename)
    
    Returns:
        Loaded Keras model
    """
    
    if model_path is None:
        if filename is None:
            filename = config.MODEL_FILENAME
        model_path = os.path.join(config.SAVED_MODELS_DIR, filename)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")
    
    model = keras.models.load_model(model_path)
    print(f"Model loaded from: {model_path}")
    
    return model


def convert_to_tflite(model, filename=None, quantize=False):
    """
    Convert Keras model to TensorFlow Lite format
    
    Args:
        model: Keras model or path to saved model
        filename: Output filename for TFLite model
        quantize: Whether to apply post-training quantization
    
    Returns:
        Path to TFLite model
    """
    
    if filename is None:
        filename = config.TFLITE_FILENAME
    
    # Load model if path is provided
    if isinstance(model, str):
        model = load_model(model_path=model)
    
    # Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        print("Applying post-training quantization...")
    
    tflite_model = converter.convert()
    
    # Save TFLite model
    tflite_path = os.path.join(config.SAVED_MODELS_DIR, filename)
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"TFLite model saved to: {tflite_path}")
    
    # Print size comparison
    if isinstance(model, keras.Model):
        original_size = os.path.getsize(config.get_model_path()) / (1024 * 1024)
        tflite_size = os.path.getsize(tflite_path) / (1024 * 1024)
        print(f"Original model size: {original_size:.2f} MB")
        print(f"TFLite model size: {tflite_size:.2f} MB")
        print(f"Size reduction: {(1 - tflite_size/original_size) * 100:.1f}%")
    
    return tflite_path


def convert_to_onnx(model, filename=None):
    """
    Convert Keras model to ONNX format
    
    Args:
        model: Keras model or path to saved model
        filename: Output filename for ONNX model
    
    Returns:
        Path to ONNX model
    """
    
    try:
        import tf2onnx
    except ImportError:
        print("tf2onnx not installed. Install with: pip install tf2onnx")
        return None
    
    if filename is None:
        filename = config.ONNX_FILENAME
    
    # Load model if path is provided
    if isinstance(model, str):
        model = load_model(model_path=model)
    
    # Convert to ONNX
    onnx_path = os.path.join(config.SAVED_MODELS_DIR, filename)
    
    spec = (tf.TensorSpec((None, *config.INPUT_SHAPE), tf.float32, name="input"),)
    model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec)
    
    with open(onnx_path, "wb") as f:
        f.write(model_proto.SerializeToString())
    
    print(f"ONNX model saved to: {onnx_path}")
    return onnx_path


def print_model_info(model):
    """
    Print detailed information about the model
    
    Args:
        model: Keras model
    """
    
    print("\n" + "=" * 70)
    print("MODEL INFORMATION")
    print("=" * 70)
    
    model.summary()
    
    print("\n" + "-" * 70)
    print("Layer Details:")
    print("-" * 70)
    
    for i, layer in enumerate(model.layers):
        print(f"{i+1}. {layer.name:20s} | Type: {layer.__class__.__name__:20s} | Output: {layer.output_shape}")
    
    print("\n" + "-" * 70)
    print("Parameter Count:")
    print("-" * 70)
    
    trainable = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    non_trainable = sum([tf.keras.backend.count_params(w) for w in model.non_trainable_weights])
    total = trainable + non_trainable
    
    print(f"Trainable:     {trainable:,}")
    print(f"Non-trainable: {non_trainable:,}")
    print(f"Total:         {total:,}")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    """Test model utilities"""
    
    from cnn_model import create_emotion_model
    
    print("Testing model utilities...")
    
    # Create a test model
    model = create_emotion_model()
    print_model_info(model)
    
    # Test saving
    print("\nTesting save functionality...")
    save_model(model, filename='test_model.h5')
    
    # Test loading
    print("\nTesting load functionality...")
    loaded_model = load_model(filename='test_model.h5')
    
    print("\nModel utilities test completed!")
