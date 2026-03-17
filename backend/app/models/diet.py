from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class DietRecord(Base):
    __tablename__ = "diet_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Meal info
    meal_type = Column(String(20), nullable=False)  # breakfast/lunch/dinner/snack
    record_date = Column(DateTime, nullable=False)
    
    # Food details
    food_name = Column(String(200), nullable=False)
    food_description = Column(Text, nullable=True)
    
    # Nutrition (per serving)
    calories = Column(Float, nullable=True)  # kcal
    protein_g = Column(Float, nullable=True)  # grams
    carbs_g = Column(Float, nullable=True)  # grams
    fat_g = Column(Float, nullable=True)  # grams
    fiber_g = Column(Float, nullable=True)  # grams
    sodium_mg = Column(Float, nullable=True)  # milligrams
    
    # Portion
    portion_size = Column(String(50), nullable=True)  # e.g., "1 bowl", "200g"
    
    # Photo
    photo_url = Column(String(500), nullable=True)
    
    # Additional notes
    notes = Column(Text, nullable=True)
    
    # Source (manual entry or AI estimation)
    source = Column(String(20), default="manual")  # manual / ai_estimated
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="diet_records")

    def __repr__(self):
        return f"<DietRecord(id={self.id}, meal={self.meal_type}, food={self.food_name})>"
