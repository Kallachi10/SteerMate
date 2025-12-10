"""Traffic Sign Detector for backend processing.

This module provides server-side sign detection using a TensorFlow/PyTorch model.
For real-time detection, the mobile app uses TFLite on-device.
This is primarily for:
- Batch processing of uploaded trip images
- Validation and testing
- Generating training data
"""

import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Model configuration
MODEL_DIR = Path(__file__).parent / "models"
TFLITE_MODEL_PATH = MODEL_DIR / "traffic_signs.tflite"
LABELS_PATH = MODEL_DIR / "labels.txt"

# Detection configuration
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
INPUT_SIZE = (224, 224)  # MobileNetV2 input size


class SignDetector:
    """Server-side traffic sign detector.
    
    This class wraps the ML model for traffic sign detection.
    It can be used for batch processing or validation.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the sign detector.
        
        Args:
            model_path: Path to the TFLite model file (optional)
        """
        self.model_path = model_path or str(TFLITE_MODEL_PATH)
        self.interpreter = None
        self.labels = []
        self._loaded = False
        
    def load(self) -> bool:
        """Load the model for inference.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        if self._loaded:
            return True
            
        if not os.path.exists(self.model_path):
            logger.warning(f"Model file not found: {self.model_path}")
            logger.info("To use sign detection, download a trained model to ml/models/")
            return False
            
        try:
            # Try to import TensorFlow Lite
            import tensorflow as tf
            
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            
            # Load labels if available
            if os.path.exists(LABELS_PATH):
                with open(LABELS_PATH, 'r') as f:
                    self.labels = [line.strip() for line in f.readlines()]
            
            self._loaded = True
            logger.info(f"Loaded sign detection model from {self.model_path}")
            return True
            
        except ImportError:
            logger.warning("TensorFlow not installed. Install with: pip install tensorflow")
            return False
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def detect(self, image_bytes: bytes, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD) -> list[dict]:
        """Detect traffic signs in an image.
        
        Args:
            image_bytes: Raw image bytes (JPEG or PNG)
            confidence_threshold: Minimum confidence for detections
            
        Returns:
            List of detections with class, confidence, and bounding box
        """
        if not self._loaded and not self.load():
            return []
            
        try:
            import numpy as np
            from PIL import Image
            import io
            
            # Decode image
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            image = image.resize(INPUT_SIZE)
            
            # Prepare input
            input_data = np.expand_dims(np.array(image, dtype=np.float32) / 255.0, axis=0)
            
            # Run inference
            input_details = self.interpreter.get_input_details()
            output_details = self.interpreter.get_output_details()
            
            self.interpreter.set_tensor(input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            # Get output
            output = self.interpreter.get_tensor(output_details[0]['index'])[0]
            
            # Process results (classification model returns probabilities)
            detections = []
            for class_id, confidence in enumerate(output):
                if confidence >= confidence_threshold:
                    detections.append({
                        "class_id": class_id,
                        "class_name": self.labels[class_id] if class_id < len(self.labels) else f"class_{class_id}",
                        "confidence": float(confidence),
                    })
            
            # Sort by confidence
            detections.sort(key=lambda x: x["confidence"], reverse=True)
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if the detector is available (model loaded)."""
        return self._loaded or os.path.exists(self.model_path)


# Singleton instance
_detector: Optional[SignDetector] = None


def get_detector() -> SignDetector:
    """Get the singleton sign detector instance."""
    global _detector
    if _detector is None:
        _detector = SignDetector()
    return _detector
