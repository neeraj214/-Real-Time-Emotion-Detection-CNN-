"""
Visualization utilities
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.facecolor'] = 'white'


def plot_emotion_distribution(y, title='Emotion Distribution', save_path=None):
    """
    Plot emotion class distribution
    
    Args:
        y: Labels (one-hot or integer)
        title: Plot title
        save_path: Path to save plot
    """
    
    # Convert one-hot to integer if needed
    if len(y.shape) > 1:
        y = np.argmax(y, axis=1)
    
    # Count emotions
    unique, counts = np.unique(y, return_counts=True)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(unique)))
    bars = ax.bar(
        [config.EMOTION_LABELS[i] for i in unique],
        counts,
        color=colors,
        edgecolor='black',
        linewidth=1.5
    )
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Emotion', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_sample_images(X, y, num_samples=25, title='Sample Images', save_path=None):
    """
    Plot sample images with labels
    
    Args:
        X: Images
        y: Labels
        num_samples: Number of samples to plot
        title: Plot title
        save_path: Path to save plot
    """
    
    # Convert one-hot to integer if needed
    if len(y.shape) > 1:
        y = np.argmax(y, axis=1)
    
    # Get random samples
    indices = np.random.choice(len(X), min(num_samples, len(X)), replace=False)
    
    # Calculate grid size
    grid_size = int(np.ceil(np.sqrt(num_samples)))
    
    fig, axes = plt.subplots(grid_size, grid_size, figsize=(12, 12))
    
    for i, ax in enumerate(axes.flat):
        if i < len(indices):
            idx = indices[i]
            img = X[idx].squeeze()
            label = config.EMOTION_LABELS[y[idx]]
            
            ax.imshow(img, cmap='gray')
            ax.set_title(label, fontsize=10, fontweight='bold')
            ax.axis('off')
        else:
            ax.axis('off')
    
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_model_architecture(model, save_path=None):
    """
    Plot model architecture
    
    Args:
        model: Keras model
        save_path: Path to save plot
    """
    
    try:
        from tensorflow.keras.utils import plot_model
        
        if save_path is None:
            save_path = 'model_architecture.png'
        
        plot_model(
            model,
            to_file=save_path,
            show_shapes=True,
            show_layer_names=True,
            rankdir='TB',
            expand_nested=True,
            dpi=150
        )
        
        print(f"Model architecture plot saved to: {save_path}")
        
    except Exception as e:
        print(f"Could not plot model architecture: {e}")
        print("Install graphviz and pydot: pip install pydot graphviz")


if __name__ == '__main__':
    """Test visualization utilities"""
    
    print("Testing visualization utilities...")
    
    # Test emotion distribution plot
    y_test = np.random.randint(0, config.NUM_CLASSES, 1000)
    plot_emotion_distribution(y_test, save_path='test_distribution.png')
    
    # Test sample images plot
    X_test = np.random.rand(100, 48, 48, 1)
    plot_sample_images(X_test, y_test, num_samples=16, save_path='test_samples.png')
    
    print("\n✓ Visualization utilities test completed!")
