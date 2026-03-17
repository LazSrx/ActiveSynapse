from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class MuscleGroup(str, enum.Enum):
    CHEST = "chest"           # 胸
    BACK = "back"             # 背
    LEGS = "legs"             # 腿
    SHOULDERS = "shoulders"   # 肩
    ARMS = "arms"             # 手臂
    CORE = "core"             # 核心
    FULL_BODY = "full_body"   # 全身


class StrengthTrainingRecord(Base):
    __tablename__ = "strength_training_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Workout info
    workout_date = Column(DateTime, nullable=False)
    exercise_name = Column(String(100), nullable=False)
    muscle_group = Column(String(30), nullable=False)  # chest/back/legs/shoulders/arms/core
    
    # Sets and reps
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=True)  # Can be null for timed exercises
    weight_kg = Column(Float, nullable=True)  # Can be null for bodyweight exercises
    
    # Alternative metrics
    duration_minutes = Column(Float, nullable=True)  # For timed exercises like planks
    distance_m = Column(Float, nullable=True)  # For exercises like sled push
    
    # Volume calculation (sets * reps * weight)
    total_volume = Column(Float, nullable=True)
    
    # RPE (Rate of Perceived Exertion) 1-10
    rpe = Column(Integer, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Tags for categorization
    tags = Column(JSON, nullable=True)  # ["compound", "isolation", "bodyweight"]
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="strength_records")

    def __repr__(self):
        return f"<StrengthTrainingRecord(id={self.id}, exercise={self.exercise_name}, group={self.muscle_group})>"


# Predefined exercise library (optional reference table)
class ExerciseLibrary(Base):
    __tablename__ = "exercise_library"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), nullable=False, unique=True)
    name_cn = Column(String(100), nullable=True)  # Chinese name
    muscle_group = Column(String(30), nullable=False)
    
    # Exercise type
    exercise_type = Column(String(30), nullable=True)  # compound/isolation/bodyweight/cardio
    equipment = Column(String(50), nullable=True)  # barbell/dumbbell/machine/bodyweight/cable
    
    # Description
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    
    # Media
    video_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    
    # Difficulty
    difficulty = Column(String(20), nullable=True)  # beginner/intermediate/advanced
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<ExerciseLibrary(id={self.id}, name={self.name})>"
