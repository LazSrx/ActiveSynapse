from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class StrengthRecordBase(BaseModel):
    workout_date: datetime
    exercise_name: str = Field(..., min_length=1, max_length=100)
    muscle_group: str = Field(..., description="Muscle group: chest, back, legs, shoulders, arms, core")
    sets: int = Field(..., ge=1)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[float] = Field(None, ge=0)
    distance_m: Optional[float] = Field(None, ge=0)
    total_volume: Optional[float] = None
    rpe: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class StrengthRecordCreate(StrengthRecordBase):
    pass


class StrengthRecordUpdate(BaseModel):
    workout_date: Optional[datetime] = None
    exercise_name: Optional[str] = Field(None, min_length=1, max_length=100)
    muscle_group: Optional[str] = None
    sets: Optional[int] = Field(None, ge=1)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[float] = Field(None, ge=0)
    distance_m: Optional[float] = Field(None, ge=0)
    total_volume: Optional[float] = None
    rpe: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class StrengthRecordResponse(StrengthRecordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Exercise Library Schema
class ExerciseLibraryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    name_cn: Optional[str] = None
    muscle_group: str
    exercise_type: Optional[str] = None  # compound/isolation/bodyweight/cardio
    equipment: Optional[str] = None  # barbell/dumbbell/machine/bodyweight/cable
    description: Optional[str] = None
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    difficulty: Optional[str] = None  # beginner/intermediate/advanced


class ExerciseLibraryCreate(ExerciseLibraryBase):
    pass


class ExerciseLibraryResponse(ExerciseLibraryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Strength Statistics Schema
class MuscleGroupStats(BaseModel):
    muscle_group: str
    total_sets: int
    total_volume: float
    session_count: int


class StrengthStatistics(BaseModel):
    total_workouts: int
    total_sets: int
    total_volume: float
    muscle_group_stats: List[MuscleGroupStats]
    recent_exercises: List[str]
