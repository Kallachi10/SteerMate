"""Pydantic schemas for trips, events, and sign detections."""

from datetime import datetime

from pydantic import BaseModel, Field


class TripEventCreate(BaseModel):
    """Schema for creating a trip event."""
    event_type: str = Field(..., description="Type of event: hard_brake, overspeed, harsh_accel, unsafe_curve")
    timestamp: datetime | None = None
    lat: float | None = None
    lon: float | None = None
    speed_m_s: float | None = None
    accel_m_s2: float | None = None


class TripEventResponse(BaseModel):
    """Schema for trip event response."""
    id: int
    event_type: str
    timestamp: datetime | None
    lat: float | None
    lon: float | None
    speed_m_s: float | None
    accel_m_s2: float | None
    
    class Config:
        from_attributes = True


class SignDetectionCreate(BaseModel):
    """Schema for creating a sign detection."""
    ts: datetime | None = None
    sign_class: str = Field(..., description="Detected sign class, e.g. 'speed_limit_60'")
    confidence: float | None = None
    bbox: dict | None = Field(None, description="Bounding box as JSON: {x, y, width, height}")


class SignDetectionResponse(BaseModel):
    """Schema for sign detection response."""
    id: int
    ts: datetime | None
    sign_class: str
    confidence: float | None
    bbox: dict | None
    
    class Config:
        from_attributes = True


class TripUpload(BaseModel):
    """Schema for uploading a complete trip."""
    start_time: datetime
    end_time: datetime
    duration_seconds: int | None = None
    distance_m: float | None = None
    avg_speed_m_s: float | None = None
    max_speed_m_s: float | None = None
    events: list[TripEventCreate] = Field(default_factory=list)
    sign_detections: list[SignDetectionCreate] = Field(default_factory=list)


class TripResponse(BaseModel):
    """Schema for trip response."""
    id: int
    user_id: int
    start_time: datetime | None
    end_time: datetime | None
    duration_seconds: int | None
    distance_m: float | None
    avg_speed_m_s: float | None
    max_speed_m_s: float | None
    unsafe_events: int | None
    created_at: datetime
    events: list[TripEventResponse] = Field(default_factory=list)
    sign_detections: list[SignDetectionResponse] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class TripSummary(BaseModel):
    """Schema for trip summary (without detailed events)."""
    id: int
    start_time: datetime | None
    end_time: datetime | None
    duration_seconds: int | None
    distance_m: float | None
    avg_speed_m_s: float | None
    max_speed_m_s: float | None
    unsafe_events: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TripReport(BaseModel):
    """Schema for trip report with analytics and safety scoring."""
    trip: TripResponse
    summary: dict = Field(default_factory=dict, description="Summary statistics")
    recommendations: list[str] = Field(default_factory=list, description="Personalized recommendations")
    
    # Safety scoring (Phase 2)
    safety_score: int = Field(100, ge=0, le=100, description="Overall safety score 0-100")
    risk_level: str = Field("low", description="Risk level: low, medium, high")
    grade: str = Field("A", description="Letter grade: A, B, C, D, F")
    issues: list[str] = Field(default_factory=list, description="Detected driving issues")
    score_breakdown: dict = Field(default_factory=dict, description="Score breakdown by category")
