"""
Helper script to download FER-2013 dataset
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


def print_instructions():
    """Print download instructions"""
    
    print("\n" + "=" * 70)
    print("FER-2013 DATASET DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    
    print("\nOption 1: Manual Download (Recommended)")
    print("-" * 70)
    print("1. Visit: https://www.kaggle.com/datasets/msambare/fer2013")
    print("2. Click 'Download' button")
    print("3. Extract fer2013.csv from the downloaded ZIP file")
    print(f"4. Place fer2013.csv in: {config.RAW_DATA_DIR}")
    
    print("\nOption 2: Kaggle API (Requires Setup)")
    print("-" * 70)
    print("1. Install Kaggle CLI:")
    print("   pip install kaggle")
    print("\n2. Set up Kaggle API credentials:")
    print("   a. Go to https://www.kaggle.com/account")
    print("   b. Click 'Create New API Token'")
    print("   c. Download kaggle.json")
    print("   d. Place kaggle.json in:")
    print("      Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json")
    print("      Linux/Mac: ~/.kaggle/kaggle.json")
    print("\n3. Run the download command:")
    print(f"   kaggle datasets download -d {config.FER2013_KAGGLE_DATASET}")
    print(f"   unzip fer2013.zip -d {config.RAW_DATA_DIR}")
    
    print("\n" + "=" * 70)
    print("DATASET INFORMATION")
    print("=" * 70)
    print("Dataset: FER-2013 (Facial Expression Recognition)")
    print("Size: ~60 MB")
    print("Images: 35,887 grayscale images (48x48 pixels)")
    print("Classes: 7 emotions (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)")
    print("Format: CSV file with 'emotion' and 'pixels' columns")
    print("=" * 70 + "\n")


def check_dataset():
    """Check if dataset exists"""
    
    csv_path = config.get_data_path(config.FER2013_CSV_FILENAME)
    
    if os.path.exists(csv_path):
        print(f"\n✓ Dataset found at: {csv_path}")
        
        # Get file size
        size_mb = os.path.getsize(csv_path) / (1024 * 1024)
        print(f"  File size: {size_mb:.2f} MB")
        
        return True
    else:
        print(f"\n✗ Dataset not found at: {csv_path}")
        return False


def download_with_kaggle():
    """Attempt to download using Kaggle API"""
    
    try:
        import kaggle
    except ImportError:
        print("\n✗ Kaggle package not installed")
        print("Install with: pip install kaggle")
        return False
    
    try:
        print("\nDownloading FER-2013 dataset using Kaggle API...")
        print("This may take a few minutes...")
        
        # Ensure directory exists
        config.ensure_dirs()
        
        # Download dataset
        kaggle.api.dataset_download_files(
            config.FER2013_KAGGLE_DATASET,
            path=config.RAW_DATA_DIR,
            unzip=True
        )
        
        print("\n✓ Download complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        print("\nPlease ensure:")
        print("1. Kaggle API credentials are set up correctly")
        print("2. You have accepted the dataset's terms on Kaggle website")
        return False


def main():
    """Main function"""
    
    print_instructions()
    
    # Check if dataset already exists
    if check_dataset():
        print("\nDataset is already downloaded and ready to use!")
        return
    
    # Ask user if they want to try Kaggle API
    print("\nWould you like to try downloading with Kaggle API? (y/n)")
    response = input("> ").strip().lower()
    
    if response == 'y':
        success = download_with_kaggle()
        
        if success:
            check_dataset()
        else:
            print("\nPlease download manually using Option 1 above.")
    else:
        print("\nPlease download manually using the instructions above.")


if __name__ == '__main__':
    main()
