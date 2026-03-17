from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class SuggestionType(str, enum.Enum):
    TRAINING = "training"
    DIET = "diet"
    RECOVERY = "recovery"
    INJURY_PREVENTION = "injury_prevention"
    GENERAL = "general"


class PlanType(str, enum.Enum):
    RUNNING = "running"
    STRENGTH = "strength"
    BADMINTON = "badminton"
    COMBINED = "combined"


class PlanStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class AISuggestion(Base):
    __tablename__ = "ai_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Suggestion details
    suggestion_type = Column(String(30), nullable=False)  # training/diet/recovery/injury_prevention
    title = Column(String(200), nullable=True)
    
    # Context used to generate the suggestion
    context = Column(JSON, nullable=True)  # {user_profile, recent_activities, injuries, etc.}
    
    # The actual suggestion content
    suggestion_content = Column(Text, nullable=False)
    
    # User feedback
    user_feedback = Column(String(20), nullable=True)  # helpful/not_helpful
    feedback_comment = Column(Text, nullable=True)
    
    # Expiration
    expires_at = Column(DateTime, nullable=True)
    
    # Metadata
    ai_model = Column(String(50), nullable=True)  # gpt-4, etc.
    prompt_version = Column(String(20), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="ai_suggestions")

    def __repr__(self):
        return f"<AISuggestion(id={self.id}, type={self.suggestion_type})>"


class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Plan details
    plan_name = Column(String(200), nullable=False)
    plan_type = Column(String(30), nullable=False)  # running/strength/badminton/combined
    
    # Timeline
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Status
    status = Column(String(20), default="active")  # active/completed/paused/cancelled
    
    # Plan content (structured JSON)
    plan_content = Column(JSON, nullable=False)
    # Example structure:
    # {
    #   "weeks": [
    #     {
    #       "week_number": 1,
    #       "days": [
    #         {
    #           "day": "Monday",
    #           "activities": [
    #             {"type": "running", "duration": 30, "intensity": "easy", "description": "..."}
    #           ]
    #         }
    #       ]
    #     }
    #   ],
    #   "goals": ["improve endurance", "build strength"],
    #   "notes": "..."
    # }
    
    # AI generated flag
    ai_generated = Column(Boolean, default=False)
    ai_model = Column(String(50), nullable=True)
    
    # Progress tracking
    completed_sessions = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="training_plans")

    def __repr__(self):
        return f"<TrainingPlan(id={self.id}, name={self.plan_name}, type={self.plan_type})>"
