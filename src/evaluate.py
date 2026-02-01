"""
Model evaluation utilities
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, 
    accuracy_score, precision_recall_fscore_support
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from models.model_utils import load_model
from src.data_preprocessing import load_and_preprocess_fer2013


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model on test set
    
    Args:
        model: Trained Keras model
        X_test: Test images
        y_test: Test labels (one-hot encoded)
    
    Returns:
        Dictionary with evaluation metrics
    """
    
    print("\n" + "=" * 70)
    print("EVALUATING MODEL")
    print("=" * 70)
    
    # Get predictions
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = np.argmax(y_test, axis=1)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average='weighted'
    )
    
    print(f"\nTest Set Performance:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    
    # Per-class metrics
    print("\n" + "-" * 70)
    print("Per-Class Metrics:")
    print("-" * 70)
    
    report = classification_report(
        y_true, y_pred,
        target_names=list(config.EMOTION_LABELS.values()),
        digits=4
    )
    print(report)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    results = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'y_true': y_true,
        'y_pred': y_pred,
        'y_pred_probs': y_pred_probs
    }
    
    return results


def plot_confusion_matrix(cm, save_path=None):
    """
    Plot confusion matrix
    
    Args:
        cm: Confusion matrix
        save_path: Path to save plot
    """
    
    if save_path is None:
        save_path = os.path.join(config.SAVED_MODELS_DIR, config.CONFUSION_MATRIX_FILENAME)
    
    plt.figure(figsize=(10, 8))
    
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=list(config.EMOTION_LABELS.values()),
        yticklabels=list(config.EMOTION_LABELS.values()),
        cbar_kws={'label': 'Count'}
    )
    
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicted Emotion', fontsize=12, fontweight='bold')
    plt.ylabel('True Emotion', fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nConfusion matrix saved to: {save_path}")
    
    plt.close()


def visualize_predictions(model, X_test, y_test, num_samples=16):
    """
    Visualize sample predictions
    
    Args:
        model: Trained model
        X_test: Test images
        y_test: Test labels
        num_samples: Number of samples to visualize
    """
    
    # Get random samples
    indices = np.random.choice(len(X_test), num_samples, replace=False)
    
    # Get predictions
    y_pred_probs = model.predict(X_test[indices], verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = np.argmax(y_test[indices], axis=1)
    
    # Plot
    rows = 4
    cols = 4
    fig, axes = plt.subplots(rows, cols, figsize=(12, 12))
    
    for i, ax in enumerate(axes.flat):
        if i < len(indices):
            # Display image
            img = X_test[indices[i]].squeeze()
            ax.imshow(img, cmap='gray')
            
            # Get labels
            true_label = config.EMOTION_LABELS[y_true[i]]
            pred_label = config.EMOTION_LABELS[y_pred[i]]
            confidence = y_pred_probs[i][y_pred[i]]
            
            # Set title color based on correctness
            color = 'green' if y_true[i] == y_pred[i] else 'red'
            
            ax.set_title(
                f'True: {true_label}\nPred: {pred_label} ({confidence:.2f})',
                fontsize=9,
                color=color
            )
            ax.axis('off')
        else:
            ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(
        os.path.join(config.SAVED_MODELS_DIR, 'sample_predictions.png'),
        dpi=150,
        bbox_inches='tight'
    )
    print("Sample predictions saved to: sample_predictions.png")
    plt.close()


if __name__ == '__main__':
    """Main evaluation script"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate emotion detection model')
    parser.add_argument('--model-path', type=str, default=None,
                        help='Path to trained model')
    parser.add_argument('--data-path', type=str, default=None,
                        help='Path to FER-2013 CSV file')
    
    args = parser.parse_args()
    
    try:
        # Load model
        print("Loading model...")
        if args.model_path:
            model = load_model(model_path=args.model_path)
        else:
            model = load_model()
        
        # Load data
        print("Loading test data...")
        data = load_and_preprocess_fer2013(csv_path=args.data_path)
        X_test = data['X_test']
        y_test = data['y_test']
        
        # Evaluate
        results = evaluate_model(model, X_test, y_test)
        
        # Plot confusion matrix
        if config.SAVE_CONFUSION_MATRIX:
            plot_confusion_matrix(results['confusion_matrix'])
        
        # Visualize predictions
        visualize_predictions(model, X_test, y_test)
        
        print("\n" + "=" * 70)
        print("EVALUATION COMPLETE")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        
    except Exception as e:
        print(f"\n✗ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
