# Traffic Sign Detection Training

This folder contains scripts and data for training the traffic sign detection model.

## Quick Start

### Option 1: Use Pre-trained Model (Fastest)

```bash
python scripts/download_pretrained.py
```

### Option 2: Train Your Own Model

```bash
# 1. Download GTSRB dataset from Kaggle
# https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign

# 2. Convert to YOLO format
python scripts/convert_gtsrb_to_yolo.py

# 3. Train YOLOv8
python scripts/train_yolov8.py

# 4. Export to TFLite
python scripts/export_tflite.py
```

## Folder Structure

```
training/
├── data/           # Training data (GTSRB images)
├── models/         # Trained model checkpoints
├── scripts/        # Training and conversion scripts
└── README.md       # This file
```

## Requirements

```bash
pip install ultralytics torch torchvision tflite-support
```
