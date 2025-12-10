from datetime import datetime

from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base


class Trip(Base):
    """Trip summary model."""
    
    __tablename__ = "trips"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    distance_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_speed_m_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_speed_m_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    unsafe_events: Mapped[int | None] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    events: Mapped[list["TripEvent"]] = relationship(back_populates="trip", cascade="all, delete-orphan")
    sign_detections: Mapped[list["SignDetection"]] = relationship(back_populates="trip", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Trip(id={self.id}, user_id={self.user_id})>"


class TripEvent(Base):
    """Unsafe driving event model (hard brake, overspeed, etc.)."""
    
    __tablename__ = "trip_events"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'hard_brake', 'overspeed', etc.
    timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    speed_m_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    accel_m_s2: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Relationship
    trip: Mapped["Trip"] = relationship(back_populates="events")
    
    def __repr__(self) -> str:
        return f"<TripEvent(id={self.id}, type={self.event_type})>"


class SignDetection(Base):
    """Traffic sign detection model."""
    
    __tablename__ = "sign_detections"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False, index=True)
    ts: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sign_class: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. 'speed_limit_60'
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    bbox: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Bounding box as JSON
    
    # Relationship
    trip: Mapped["Trip"] = relationship(back_populates="sign_detections")
    
    def __repr__(self) -> str:
        return f"<SignDetection(id={self.id}, class={self.sign_class})>"
