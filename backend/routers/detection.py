"""Sign Detection API Router.

Provides endpoints for:
- Getting sign class information
- Server-side sign detection (for testing/validation)
- Model info and download
"""

import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse

from ml.sign_classes import (
    GTSRB_CLASSES, 
    SPEED_LIMIT_CLASSES, 
    WARNING_CLASSES,
    get_speed_limit_value,
    get_class_name,
)
from ml.detector import get_detector, MODEL_DIR, TFLITE_MODEL_PATH
from schemas.detection import (
    SignClassInfo, 
    DetectionResult, 
    DetectionResponse, 
    ModelInfo,
)

router = APIRouter(prefix="/detection", tags=["Sign Detection"])


@router.get("/classes", response_model=list[SignClassInfo])
async def list_sign_classes():
    """Get all traffic sign classes with their metadata."""
    classes = []
    
    for class_id, name in GTSRB_CLASSES.items():
        # Determine category
        if class_id in SPEED_LIMIT_CLASSES:
            category = "speed_limit"
        elif class_id in WARNING_CLASSES:
            category = "warning"
        elif class_id in [9, 10, 15, 16, 17]:
            category = "regulatory"
        else:
            category = "informational"
        
        classes.append(SignClassInfo(
            class_id=class_id,
            name=name,
            category=category,
            speed_limit_kmh=get_speed_limit_value(class_id),
        ))
    
    return classes


@router.get("/classes/{class_id}", response_model=SignClassInfo)
async def get_sign_class(class_id: int):
    """Get details for a specific sign class."""
    if class_id not in GTSRB_CLASSES:
        raise HTTPException(status_code=404, detail=f"Class {class_id} not found")
    
    name = get_class_name(class_id)
    
    if class_id in SPEED_LIMIT_CLASSES:
        category = "speed_limit"
    elif class_id in WARNING_CLASSES:
        category = "warning"
    elif class_id in [9, 10, 15, 16, 17]:
        category = "regulatory"
    else:
        category = "informational"
    
    return SignClassInfo(
        class_id=class_id,
        name=name,
        category=category,
        speed_limit_kmh=get_speed_limit_value(class_id),
    )


@router.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the ML model."""
    detector = get_detector()
    
    return ModelInfo(
        name="GTSRB Traffic Sign Classifier",
        version="1.0.0",
        input_size=[224, 224, 3],
        num_classes=43,
        available=detector.is_available(),
    )


@router.get("/model/download")
async def download_model():
    """Download the TFLite model for on-device inference."""
    if not Path(TFLITE_MODEL_PATH).exists():
        raise HTTPException(
            status_code=404, 
            detail="Model file not available. Please train or download a model first."
        )
    
    return FileResponse(
        path=str(TFLITE_MODEL_PATH),
        filename="traffic_signs.tflite",
        media_type="application/octet-stream",
    )


@router.post("/detect", response_model=DetectionResponse)
async def detect_signs(
    image: UploadFile = File(...),
    confidence_threshold: float = Query(0.5, ge=0.0, le=1.0),
):
    """Detect traffic signs in an uploaded image.
    
    This endpoint is for testing/validation. For real-time detection,
    use the on-device TFLite model in the mobile app.
    """
    # Validate file type
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    start_time = time.time()
    
    # Read image
    image_bytes = await image.read()
    
    # Run detection
    detector = get_detector()
    if not detector.is_available():
        raise HTTPException(
            status_code=503, 
            detail="Sign detection model not available"
        )
    
    raw_detections = detector.detect(image_bytes, confidence_threshold)
    
    # Convert to response format
    detections = [
        DetectionResult(
            class_id=d["class_id"],
            class_name=d["class_name"],
            confidence=d["confidence"],
            bbox=d.get("bbox"),
        )
        for d in raw_detections
    ]
    
    # Find speed limit if any
    speed_limit = None
    for d in detections:
        limit = get_speed_limit_value(d.class_id)
        if limit is not None:
            speed_limit = limit
            break  # Use the most confident speed limit sign
    
    processing_time = (time.time() - start_time) * 1000
    
    return DetectionResponse(
        detections=detections,
        speed_limit=speed_limit,
        processing_time_ms=processing_time,
    )


@router.get("/speed-limits")
async def get_speed_limit_classes():
    """Get all speed limit sign classes with their km/h values."""
    return {
        class_id: {
            "name": get_class_name(class_id),
            "speed_kmh": speed,
        }
        for class_id, speed in SPEED_LIMIT_CLASSES.items()
        if speed is not None
    }
