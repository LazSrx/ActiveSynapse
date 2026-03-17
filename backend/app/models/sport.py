from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class SportType(str, enum.Enum):
    RUNNING = "running"
    BADMINTON = "badminton"


class MatchType(str, enum.Enum):
    SINGLES = "singles"
    DOUBLES = "doubles"


class CourtType(str, enum.Enum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"


class SportRecord(Base):
    __tablename__ = "sport_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Basic info
    sport_type = Column(String(20), nullable=False)  # running / badminton
    record_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Source
    source = Column(String(20), default="manual")  # coros / manual
    gpx_file_url = Column(String(500), nullable=True)  # GPX file from COROS
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="sport_records")
    running_detail = relationship("RunningDetail", back_populates="sport_record", uselist=False, cascade="all, delete-orphan")
    badminton_detail = relationship("BadmintonDetail", back_populates="sport_record", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SportRecord(id={self.id}, type={self.sport_type}, date={self.record_date})>"


class RunningDetail(Base):
    __tablename__ = "running_details"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("sport_records.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Distance and pace
    distance_km = Column(Float, nullable=False)
    pace_min_per_km = Column(Float, nullable=True)  # Average pace
    
    # Heart rate
    heart_rate_avg = Column(Integer, nullable=True)
    heart_rate_max = Column(Integer, nullable=True)
    
    # Elevation
    elevation_gain_m = Column(Float, nullable=True)
    elevation_loss_m = Column(Float, nullable=True)
    
    # Running metrics
    cadence_avg = Column(Integer, nullable=True)  # Steps per minute
    stride_length_cm = Column(Float, nullable=True)
    
    # Weather and conditions
    weather_conditions = Column(JSON, nullable=True)  # {"temperature": 20, "humidity": 60, "condition": "sunny"}
    
    # Route data (optional, for GPX parsing)
    route_data = Column(JSON, nullable=True)  # Array of {lat, lon, elevation, time, hr}

    # Relationships
    sport_record = relationship("SportRecord", back_populates="running_detail")

    def __repr__(self):
        return f"<RunningDetail(record_id={self.record_id}, distance={self.distance_km}km)>"


class BadmintonDetail(Base):
    __tablename__ = "badminton_details"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("sport_records.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Match info
    match_type = Column(String(20), nullable=True)  # singles / doubles
    opponent_level = Column(String(20), nullable=True)  # beginner/intermediate/advanced
    score = Column(String(50), nullable=True)  # e.g., "21:18, 19:21, 21:15"
    
    # Court
    court_type = Column(String(20), nullable=True)  # indoor / outdoor
    
    # Video
    video_url = Column(String(500), nullable=True)
    
    # Highlights (timestamps of good plays)
    highlights = Column(JSON, nullable=True)  # [{"start": 120, "end": 135, "description": "great smash"}]
    
    # Match stats (if available)
    stats = Column(JSON, nullable=True)  # {"smashes": 25, "drops": 15, "clears": 30}

    # Relationships
    sport_record = relationship("SportRecord", back_populates="badminton_detail")

    def __repr__(self):
        return f"<BadmintonDetail(record_id={self.record_id}, type={self.match_type})>"
