import zipfile
import os

zip_path = 'data/raw/archive.zip'
extract_path = 'data/raw/extracted'

if not os.path.exists(extract_path):
    os.makedirs(extract_path)

print(f"Extracting {zip_path} to {extract_path}...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)
    print("Files found in zip:")
    for file in zip_ref.namelist():
        print(f"  - {file}")
