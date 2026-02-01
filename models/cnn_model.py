"""
CNN Model Architecture for Facial Emotion Detection
Lightweight model optimized for real-time CPU inference
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.regularizers import l2
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


def build_emotion_cnn(input_shape=config.INPUT_SHAPE, 
                      num_classes=config.NUM_CLASSES,
                      conv_filters=config.CONV_FILTERS,
                      dense_units=config.DENSE_UNITS,
                      dropout_rates=config.DROPOUT_RATES,
                      use_batch_norm=config.USE_BATCH_NORM):
    """
    Build a lightweight CNN for emotion classification
    
    Architecture:
    - 3 Convolutional blocks (Conv2D -> BatchNorm -> ReLU -> MaxPool)
    - 2 Dense layers with Dropout
    - Softmax output layer
    
    Args:
        input_shape: Input image shape (height, width, channels)
        num_classes: Number of emotion classes
        conv_filters: List of filter counts for each conv block
        dense_units: List of units for each dense layer
        dropout_rates: List of dropout rates for each dense layer
        use_batch_norm: Whether to use Batch Normalization
    
    Returns:
        Compiled Keras model
    """
    
    model = models.Sequential(name='EmotionCNN')
    
    # ========================================================================
    # CONVOLUTIONAL BLOCKS
    # ========================================================================
    
    # Block 1: 32 filters
    model.add(layers.Conv2D(
        conv_filters[0], 
        config.CONV_KERNEL_SIZE, 
        padding='same',
        input_shape=input_shape,
        kernel_regularizer=l2(0.0001),
        name='conv1'
    ))
    if use_batch_norm:
        model.add(layers.BatchNormalization(name='bn1'))
    model.add(layers.Activation('relu', name='relu1'))
    model.add(layers.MaxPooling2D(pool_size=config.POOL_SIZE, name='pool1'))
    model.add(layers.Dropout(0.25, name='dropout1'))
    
    # Block 2: 64 filters
    model.add(layers.Conv2D(
        conv_filters[1], 
        config.CONV_KERNEL_SIZE, 
        padding='same',
        kernel_regularizer=l2(0.0001),
        name='conv2'
    ))
    if use_batch_norm:
        model.add(layers.BatchNormalization(name='bn2'))
    model.add(layers.Activation('relu', name='relu2'))
    model.add(layers.MaxPooling2D(pool_size=config.POOL_SIZE, name='pool2'))
    model.add(layers.Dropout(0.25, name='dropout2'))
    
    # Block 3: 128 filters
    model.add(layers.Conv2D(
        conv_filters[2], 
        config.CONV_KERNEL_SIZE, 
        padding='same',
        kernel_regularizer=l2(0.0001),
        name='conv3'
    ))
    if use_batch_norm:
        model.add(layers.BatchNormalization(name='bn3'))
    model.add(layers.Activation('relu', name='relu3'))
    model.add(layers.MaxPooling2D(pool_size=config.POOL_SIZE, name='pool3'))
    model.add(layers.Dropout(0.25, name='dropout3'))
    
    # ========================================================================
    # DENSE LAYERS
    # ========================================================================
    
    model.add(layers.Flatten(name='flatten'))
    
    # Dense layer 1
    model.add(layers.Dense(
        dense_units[0], 
        kernel_regularizer=l2(0.0001),
        name='dense1'
    ))
    if use_batch_norm:
        model.add(layers.BatchNormalization(name='bn_dense1'))
    model.add(layers.Activation('relu', name='relu_dense1'))
    model.add(layers.Dropout(dropout_rates[0], name='dropout_dense1'))
    
    # Dense layer 2
    model.add(layers.Dense(
        dense_units[1], 
        kernel_regularizer=l2(0.0001),
        name='dense2'
    ))
    if use_batch_norm:
        model.add(layers.BatchNormalization(name='bn_dense2'))
    model.add(layers.Activation('relu', name='relu_dense2'))
    model.add(layers.Dropout(dropout_rates[1], name='dropout_dense2'))
    
    # ========================================================================
    # OUTPUT LAYER
    # ========================================================================
    
    model.add(layers.Dense(num_classes, activation='softmax', name='output'))
    
    return model


def compile_model(model, 
                  learning_rate=config.LEARNING_RATE,
                  optimizer=config.OPTIMIZER,
                  loss=config.LOSS,
                  metrics=config.METRICS):
    """
    Compile the model with optimizer, loss, and metrics
    
    Args:
        model: Keras model to compile
        learning_rate: Learning rate for optimizer
        optimizer: Optimizer name or instance
        loss: Loss function
        metrics: List of metrics to track
    
    Returns:
        Compiled model
    """
    
    if optimizer == 'adam':
        opt = keras.optimizers.Adam(learning_rate=learning_rate)
    elif optimizer == 'sgd':
        opt = keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9)
    elif optimizer == 'rmsprop':
        opt = keras.optimizers.RMSprop(learning_rate=learning_rate)
    else:
        opt = optimizer
    
    model.compile(
        optimizer=opt,
        loss=loss,
        metrics=metrics
    )
    
    return model


def create_emotion_model():
    """
    Create and compile the emotion detection CNN model
    
    Returns:
        Compiled Keras model ready for training
    """
    
    model = build_emotion_cnn()
    model = compile_model(model)
    
    return model


if __name__ == '__main__':
    """Test model creation and display summary"""
    
    print("=" * 70)
    print("Building Emotion Detection CNN Model")
    print("=" * 70)
    
    model = create_emotion_model()
    
    print("\nModel Summary:")
    print("-" * 70)
    model.summary()
    
    print("\n" + "=" * 70)
    print("Model Architecture Details")
    print("=" * 70)
    print(f"Input Shape: {config.INPUT_SHAPE}")
    print(f"Number of Classes: {config.NUM_CLASSES}")
    print(f"Emotion Labels: {list(config.EMOTION_LABELS.values())}")
    print(f"Total Parameters: {model.count_params():,}")
    
    # Calculate model size
    trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    non_trainable_params = sum([tf.keras.backend.count_params(w) for w in model.non_trainable_weights])
    
    print(f"Trainable Parameters: {trainable_params:,}")
    print(f"Non-trainable Parameters: {non_trainable_params:,}")
    print("=" * 70)
