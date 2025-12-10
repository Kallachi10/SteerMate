"""Pydantic schemas for sign detection endpoints."""

from pydantic import BaseModel, Field
from typing import Optional


class SignClassInfo(BaseModel):
    """Information about a traffic sign class."""
    class_id: int = Field(..., ge=0, le=42)
    name: str
    category: str  # speed_limit, warning, regulatory, informational
    speed_limit_kmh: Optional[int] = None


class DetectionResult(BaseModel):
    """Single sign detection result."""
    class_id: int
    class_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: Optional[list[float]] = None  # [x1, y1, x2, y2] normalized


class DetectionResponse(BaseModel):
    """Response from sign detection endpoint."""
    detections: list[DetectionResult]
    speed_limit: Optional[int] = None  # Detected speed limit in km/h
    processing_time_ms: float


class ModelInfo(BaseModel):
    """Information about the ML model."""
    name: str
    version: str
    input_size: list[int]
    num_classes: int
    available: bool
