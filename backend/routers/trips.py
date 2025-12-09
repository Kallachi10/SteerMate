"""Trips router for uploading trips and generating reports."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.user import User
from models.trip import Trip, TripEvent, SignDetection
from schemas.trip import TripUpload, TripResponse, TripSummary, TripReport
from utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/upload", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def upload_trip(
    trip_data: TripUpload,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a complete trip with events and sign detections."""
    # Calculate unsafe events count
    unsafe_events_count = len(trip_data.events)
    
    # Create trip
    new_trip = Trip(
        user_id=current_user.id,
        start_time=trip_data.start_time,
        end_time=trip_data.end_time,
        duration_seconds=trip_data.duration_seconds,
        distance_m=trip_data.distance_m,
        avg_speed_m_s=trip_data.avg_speed_m_s,
        max_speed_m_s=trip_data.max_speed_m_s,
        unsafe_events=unsafe_events_count,
    )
    
    db.add(new_trip)
    await db.flush()  # Get the trip ID
    
    # Add events
    for event_data in trip_data.events:
        event = TripEvent(
            trip_id=new_trip.id,
            event_type=event_data.event_type,
            timestamp=event_data.timestamp,
            lat=event_data.lat,
            lon=event_data.lon,
            speed_m_s=event_data.speed_m_s,
            accel_m_s2=event_data.accel_m_s2,
        )
        db.add(event)
    
    # Add sign detections
    for sign_data in trip_data.sign_detections:
        sign = SignDetection(
            trip_id=new_trip.id,
            ts=sign_data.ts,
            sign_class=sign_data.sign_class,
            confidence=sign_data.confidence,
            bbox=sign_data.bbox,
        )
        db.add(sign)
    
    await db.commit()
    
    # Reload trip with relationships
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.events), selectinload(Trip.sign_detections))
        .where(Trip.id == new_trip.id)
    )
    trip = result.scalar_one()
    
    return trip


@router.get("", response_model=list[TripSummary])
async def list_trips(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all trips for the current user."""
    result = await db.execute(
        select(Trip)
        .where(Trip.user_id == current_user.id)
        .order_by(Trip.created_at.desc())
    )
    trips = result.scalars().all()
    return trips


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific trip with all details."""
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.events), selectinload(Trip.sign_detections))
        .where(Trip.id == trip_id, Trip.user_id == current_user.id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    return trip


@router.get("/{trip_id}/report", response_model=TripReport)
async def get_trip_report(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a report for a specific trip with analytics, safety score, and recommendations."""
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.events), selectinload(Trip.sign_detections))
        .where(Trip.id == trip_id, Trip.user_id == current_user.id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    # Generate summary statistics
    event_types = {}
    for event in trip.events:
        event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
    
    summary = {
        "total_events": len(trip.events),
        "events_by_type": event_types,
        "signs_detected": len(trip.sign_detections),
        "duration_minutes": round((trip.duration_seconds or 0) / 60, 1),
        "distance_km": round((trip.distance_m or 0) / 1000, 2),
    }
    
    # Use ML-based safety scorer (Phase 2)
    from ml.driver_scoring import score_trip_data
    
    # Convert ORM objects to dicts for scoring
    trip_data = {
        "distance_m": trip.distance_m,
        "duration_seconds": trip.duration_seconds,
        "avg_speed_m_s": trip.avg_speed_m_s,
        "max_speed_m_s": trip.max_speed_m_s,
    }
    
    events_data = [
        {
            "event_type": e.event_type,
            "speed_m_s": e.speed_m_s,
            "accel_m_s2": e.accel_m_s2,
            "timestamp": e.timestamp,
        }
        for e in trip.events
    ]
    
    detections_data = [
        {
            "sign_class": d.sign_class,
            "confidence": d.confidence,
            "ts": d.ts,
        }
        for d in trip.sign_detections
    ]
    
    # Get safety score and recommendations
    scoring_result = score_trip_data(trip_data, events_data, detections_data)
    
    return TripReport(
        trip=trip,
        summary=summary,
        recommendations=scoring_result["recommendations"],
        safety_score=scoring_result["score"],
        risk_level=scoring_result["risk_level"],
        grade=scoring_result["grade"],
        issues=scoring_result["issues"],
        score_breakdown=scoring_result["breakdown"],
    )

