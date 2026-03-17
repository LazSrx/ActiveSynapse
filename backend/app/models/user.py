from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    injury_records = relationship("InjuryRecord", back_populates="user", cascade="all, delete-orphan")
    sport_records = relationship("SportRecord", back_populates="user", cascade="all, delete-orphan")
    diet_records = relationship("DietRecord", back_populates="user", cascade="all, delete-orphan")
    strength_records = relationship("StrengthTrainingRecord", back_populates="user", cascade="all, delete-orphan")
    ai_suggestions = relationship("AISuggestion", back_populates="user", cascade="all, delete-orphan")
    training_plans = relationship("TrainingPlan", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Basic physical info
    height_cm = Column(Integer, nullable=True)  # Height in centimeters
    weight_kg = Column(Float, nullable=True)    # Weight in kilograms
    birth_date = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)  # male/female/other
    
    # Sport related
    sport_level = Column(String(20), nullable=True)  # beginner/intermediate/advanced
    sport_goals = Column(JSON, default=list)  # ["weight_loss", "muscle_gain", "performance"]
    
    # Preferences
    preferred_sports = Column(JSON, default=list)  # ["running", "badminton", "strength"]
    weekly_target = Column(JSON, default=dict)  # {"running_km": 20, "strength_sessions": 3}
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, level={self.sport_level})>"
