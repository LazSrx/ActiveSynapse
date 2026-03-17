from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class InjuryType(str, enum.Enum):
    STRAIN = "strain"           # 拉伤
    SPRAIN = "sprain"           # 扭伤
    INFLAMMATION = "inflammation"  # 炎症
    FRACTURE = "fracture"       # 骨折
    DISLOCATION = "dislocation" # 脱臼
    TENDINITIS = "tendinitis"   # 肌腱炎
    OTHER = "other"


class BodyPart(str, enum.Enum):
    KNEE = "knee"
    ANKLE = "ankle"
    SHOULDER = "shoulder"
    WRIST = "wrist"
    ELBOW = "elbow"
    BACK = "back"
    HIP = "hip"
    HAMSTRING = "hamstring"
    QUADRICEPS = "quadriceps"
    CALF = "calf"
    ACHILLES = "achilles"
    OTHER = "other"


class Severity(str, enum.Enum):
    MILD = "mild"       # 轻度
    MODERATE = "moderate"  # 中度
    SEVERE = "severe"   # 重度


class InjuryRecord(Base):
    __tablename__ = "injury_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Injury details
    injury_type = Column(String(30), nullable=False)  # Using string for flexibility
    body_part = Column(String(30), nullable=False)
    severity = Column(String(20), nullable=False)
    
    # Timeline
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)  # Null if ongoing
    
    # Description
    description = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)  # Treatment methods
    
    # Flags
    is_recurring = Column(Boolean, default=False)  # Is this a recurring injury
    is_ongoing = Column(Boolean, default=True)  # Is the injury still ongoing
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="injury_records")

    def __repr__(self):
        return f"<InjuryRecord(id={self.id}, type={self.injury_type}, part={self.body_part})>"
