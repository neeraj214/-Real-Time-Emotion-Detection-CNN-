import os
import cv2
import pandas as pd
import numpy as np
from tqdm import tqdm

# Emotion mapping from config.py
EMOTION_MAPPING = {
    'angry': 0,
    'disgust': 1,
    'fear': 2,
    'happy': 3,
    'sad': 4,
    'surprise': 5,
    'neutral': 6
}

base_path = 'data/raw/extracted'
output_csv = 'data/raw/fer2013.csv'

data = []

# Process Train and Test folders
for usage_dir in ['train', 'test']:
    usage_path = os.path.join(base_path, usage_dir)
    if not os.path.exists(usage_path):
        continue
        
    usage_label = 'Training' if usage_dir == 'train' else 'PublicTest'
    
    print(f"Processing {usage_dir} directory...")
    for emotion_name, emotion_id in EMOTION_MAPPING.items():
        emotion_path = os.path.join(usage_path, emotion_name)
        if not os.path.exists(emotion_path):
            continue
            
        print(f"  Reading {emotion_name} images...")
        for img_name in tqdm(os.listdir(emotion_path)):
            img_path = os.path.join(emotion_path, img_name)
            
            # Read image as grayscale
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            
            # Ensure image is 48x48
            if img.shape != (48, 48):
                img = cv2.resize(img, (48, 48))
                
            # Flatten and convert to space-separated string
            pixels = ' '.join(img.flatten().astype(str))
            
            data.append({
                'emotion': emotion_id,
                'pixels': pixels,
                'Usage': usage_label
            })

print(f"Saving {len(data)} samples to {output_csv}...")
df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)
print("Conversion complete!")
