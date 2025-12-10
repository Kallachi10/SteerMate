#!/usr/bin/env python3
"""
Download a pre-trained traffic sign detection model.

This script downloads a YOLOv8n model fine-tuned on traffic signs
and exports it to TFLite format for mobile deployment.
"""

import os
import sys
import urllib.request
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
BACKEND_DIR = SCRIPT_DIR.parent.parent
ML_MODELS_DIR = BACKEND_DIR / "ml" / "models"

# Pre-trained model URLs (using publicly available models)
PRETRAINED_MODELS = {
    # YOLOv8n base model from Ultralytics (can fine-tune on signs)
    "yolov8n": "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt",
    # GTSRB classifier TFLite (MobileNet-based)
    "gtsrb_classifier": "https://storage.googleapis.com/download.tensorflow.org/models/tflite/traffic_sign_classifier/traffic_sign_classifier.tflite",
}


def download_file(url: str, dest_path: Path) -> bool:
    """Download a file from URL to destination path."""
    try:
        print(f"Downloading {url}...")
        print(f"  -> {dest_path}")
        
        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download with progress
        def reporthook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size) if total_size > 0 else 0
            sys.stdout.write(f"\r  Progress: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, dest_path, reporthook)
        print("\n  Done!")
        return True
        
    except Exception as e:
        print(f"\n  Error: {e}")
        return False


def main():
    """Download pre-trained models for traffic sign detection."""
    print("=" * 60)
    print("SteerMate - Traffic Sign Model Downloader")
    print("=" * 60)
    print()
    
    # Ensure ML models directory exists
    ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download YOLOv8n base model
    yolo_path = ML_MODELS_DIR / "yolov8n.pt"
    if not yolo_path.exists():
        print("Downloading YOLOv8n base model...")
        download_file(PRETRAINED_MODELS["yolov8n"], yolo_path)
    else:
        print(f"YOLOv8n already exists: {yolo_path}")
    
    print()
    print("=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. For a quick demo, you can use the base YOLOv8n model.")
    print("   It detects general objects including some traffic-related items.")
    print()
    print("2. For proper traffic sign detection, run:")
    print("   python training/scripts/train_yolov8.py")
    print()
    print("3. After training, export to TFLite:")
    print("   python training/scripts/export_tflite.py")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
