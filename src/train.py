"""
Training pipeline for emotion detection CNN
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from models.cnn_model import create_emotion_model
from models.model_utils import save_model
from src.data_preprocessing import load_and_preprocess_fer2013


def create_callbacks(model_name='emotion_cnn_model'):
    """
    Create training callbacks
    
    Args:
        model_name: Base name for saved model
    
    Returns:
        List of Keras callbacks
    """
    
    # Ensure directories exist
    config.ensure_dirs()
    
    # Model checkpoint - save best model
    checkpoint_path = config.get_model_path(f'{model_name}_best.h5')
    checkpoint = ModelCheckpoint(
        checkpoint_path,
        monitor=config.MONITOR_METRIC,
        save_best_only=config.SAVE_BEST_ONLY,
        mode='max',
        verbose=1
    )
    
    # Early stopping
    early_stop = EarlyStopping(
        monitor=config.MONITOR_METRIC,
        patience=config.EARLY_STOPPING_PATIENCE,
        min_delta=config.EARLY_STOPPING_MIN_DELTA,
        mode='max',
        verbose=1,
        restore_best_weights=True
    )
    
    # Reduce learning rate on plateau
    reduce_lr = ReduceLROnPlateau(
        monitor=config.MONITOR_METRIC,
        factor=config.LR_REDUCE_FACTOR,
        patience=config.LR_REDUCE_PATIENCE,
        min_lr=config.LR_MIN,
        mode='max',
        verbose=1
    )
    
    # CSV logger
    log_path = os.path.join(config.SAVED_MODELS_DIR, config.TRAINING_HISTORY_FILENAME)
    csv_logger = CSVLogger(log_path, append=False)
    
    callbacks = [checkpoint, early_stop, reduce_lr, csv_logger]
    
    print("Training callbacks configured:")
    print(f"  Model checkpoint: {checkpoint_path}")
    print(f"  Early stopping patience: {config.EARLY_STOPPING_PATIENCE}")
    print(f"  LR reduction patience: {config.LR_REDUCE_PATIENCE}")
    print(f"  CSV log: {log_path}")
    
    return callbacks


def train_model(model=None, data=None, epochs=None, batch_size=None, verbose=None):
    """
    Train the emotion detection model
    
    Args:
        model: Keras model (if None, creates new model)
        data: Dictionary with training data (if None, loads FER-2013)
        epochs: Number of training epochs
        batch_size: Batch size for training
        verbose: Verbosity level
    
    Returns:
        Trained model and training history
    """
    
    print("\n" + "=" * 70)
    print("TRAINING EMOTION DETECTION MODEL")
    print("=" * 70)
    
    # Set defaults
    if epochs is None:
        epochs = config.EPOCHS
    if batch_size is None:
        batch_size = config.BATCH_SIZE
    if verbose is None:
        verbose = config.VERBOSE
    
    # Create model if not provided
    if model is None:
        print("\nCreating model...")
        model = create_emotion_model()
        model.summary()
    
    # Load data if not provided
    if data is None:
        print("\nLoading and preprocessing data...")
        data = load_and_preprocess_fer2013()
    
    # Extract data
    X_train = data['X_train']
    y_train = data['y_train']
    X_val = data['X_val']
    y_val = data['y_val']
    train_datagen = data['train_datagen']
    
    # Create callbacks
    callbacks = create_callbacks()
    
    # Training info
    print("\n" + "=" * 70)
    print("TRAINING CONFIGURATION")
    print("=" * 70)
    print(f"Training samples:   {len(X_train):,}")
    print(f"Validation samples: {len(X_val):,}")
    print(f"Batch size:         {batch_size}")
    print(f"Epochs:             {epochs}")
    print(f"Learning rate:      {config.LEARNING_RATE}")
    print(f"Optimizer:          {config.OPTIMIZER}")
    print("=" * 70)
    
    # Start training
    print(f"\nStarting training at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)
    
    # Fit with data augmentation
    history = model.fit(
        train_datagen.flow(X_train, y_train, batch_size=batch_size),
        steps_per_epoch=len(X_train) // batch_size,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=verbose
    )
    
    print("-" * 70)
    print(f"Training completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save final model
    final_model_path = save_model(model, filename=config.MODEL_FILENAME)
    
    # Plot training history
    if config.PLOT_TRAINING_HISTORY:
        plot_training_history(history)
    
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print(f"Final model saved to: {final_model_path}")
    print(f"Best model saved during training")
    
    # Print final metrics
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    final_train_loss = history.history['loss'][-1]
    final_val_loss = history.history['val_loss'][-1]
    
    print(f"\nFinal Metrics:")
    print(f"  Training Accuracy:   {final_train_acc:.4f}")
    print(f"  Validation Accuracy: {final_val_acc:.4f}")
    print(f"  Training Loss:       {final_train_loss:.4f}")
    print(f"  Validation Loss:     {final_val_loss:.4f}")
    
    # Best metrics
    best_val_acc = max(history.history['val_accuracy'])
    best_epoch = history.history['val_accuracy'].index(best_val_acc) + 1
    
    print(f"\nBest Validation Accuracy: {best_val_acc:.4f} (Epoch {best_epoch})")
    print("=" * 70)
    
    return model, history


def plot_training_history(history, save_path=None):
    """
    Plot training history (loss and accuracy)
    
    Args:
        history: Keras History object
        save_path: Path to save plot (if None, uses config)
    """
    
    if save_path is None:
        save_path = os.path.join(config.SAVED_MODELS_DIR, config.TRAINING_PLOT_FILENAME)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot accuracy
    axes[0].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
    axes[0].plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Plot loss
    axes[1].plot(history.history['loss'], label='Train Loss', linewidth=2)
    axes[1].plot(history.history['val_loss'], label='Val Loss', linewidth=2)
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nTraining history plot saved to: {save_path}")
    
    plt.close()


if __name__ == '__main__':
    """Main training script"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Train emotion detection CNN')
    parser.add_argument('--epochs', type=int, default=config.EPOCHS,
                        help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=config.BATCH_SIZE,
                        help='Batch size for training')
    parser.add_argument('--data-path', type=str, default=None,
                        help='Path to FER-2013 CSV file')
    
    args = parser.parse_args()
    
    try:
        # Load data
        data = load_and_preprocess_fer2013(csv_path=args.data_path)
        
        # Train model
        model, history = train_model(
            data=data,
            epochs=args.epochs,
            batch_size=args.batch_size
        )
        
        print("\n✓ Training completed successfully!")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease download FER-2013 dataset:")
        print("1. Visit: https://www.kaggle.com/datasets/msambare/fer2013")
        print("2. Download fer2013.csv")
        print(f"3. Place it in: {config.RAW_DATA_DIR}")
        
    except Exception as e:
        print(f"\n✗ Training failed: {e}")
        import traceback
        traceback.print_exc()
