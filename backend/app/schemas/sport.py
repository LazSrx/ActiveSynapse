from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Running Detail Schemas
class RunningDetailBase(BaseModel):
    distance_km: float = Field(..., gt=0)
    pace_min_per_km: Optional[float] = None
    heart_rate_avg: Optional[int] = Field(None, ge=0, le=250)
    heart_rate_max: Optional[int] = Field(None, ge=0, le=250)
    elevation_gain_m: Optional[float] = None
    elevation_loss_m: Optional[float] = None
    cadence_avg: Optional[int] = None
    stride_length_cm: Optional[float] = None
    weather_conditions: Optional[Dict[str, Any]] = None
    route_data: Optional[List[Dict[str, Any]]] = None


class RunningDetailCreate(RunningDetailBase):
    pass


class RunningDetailResponse(RunningDetailBase):
    id: int
    record_id: int

    class Config:
        from_attributes = True


# Badminton Detail Schemas
class BadmintonDetailBase(BaseModel):
    match_type: Optional[str] = None  # singles/doubles
    opponent_level: Optional[str] = None  # beginner/intermediate/advanced
    score: Optional[str] = None
    court_type: Optional[str] = None  # indoor/outdoor
    video_url: Optional[str] = None
    highlights: Optional[List[Dict[str, Any]]] = None
    stats: Optional[Dict[str, Any]] = None


class BadmintonDetailCreate(BadmintonDetailBase):
    pass


class BadmintonDetailResponse(BadmintonDetailBase):
    id: int
    record_id: int

    class Config:
        from_attributes = True


# Sport Record Schemas
class SportRecordBase(BaseModel):
    sport_type: str = Field(..., description="Type: running or badminton")
    record_date: datetime
    duration_minutes: int = Field(..., gt=0)
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    source: str = "manual"  # coros or manual
    gpx_file_url: Optional[str] = None


class SportRecordCreate(SportRecordBase):
    running_detail: Optional[RunningDetailCreate] = None
    badminton_detail: Optional[BadmintonDetailCreate] = None


class SportRecordUpdate(BaseModel):
    sport_type: Optional[str] = None
    record_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    source: Optional[str] = None
    gpx_file_url: Optional[str] = None


class SportRecordResponse(SportRecordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    running_detail: Optional[RunningDetailResponse] = None
    badminton_detail: Optional[BadmintonDetailResponse] = None

    class Config:
        from_attributes = True


# Sport Statistics Schema
class SportStatistics(BaseModel):
    total_activities: int
    total_duration_minutes: int
    total_distance_km: Optional[float] = None
    total_calories: Optional[int] = None
    avg_duration_minutes: float
    avg_pace: Optional[float] = None
    avg_heart_rate: Optional[int] = None
