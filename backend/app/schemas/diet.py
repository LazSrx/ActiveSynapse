from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DietRecordBase(BaseModel):
    meal_type: str = Field(..., description="Type: breakfast, lunch, dinner, snack")
    record_date: datetime
    food_name: str = Field(..., min_length=1, max_length=200)
    food_description: Optional[str] = None
    calories: Optional[float] = Field(None, ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    fiber_g: Optional[float] = Field(None, ge=0)
    sodium_mg: Optional[float] = Field(None, ge=0)
    portion_size: Optional[str] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None
    source: str = "manual"  # manual or ai_estimated


class DietRecordCreate(DietRecordBase):
    pass


class DietRecordUpdate(BaseModel):
    meal_type: Optional[str] = None
    record_date: Optional[datetime] = None
    food_name: Optional[str] = Field(None, min_length=1, max_length=200)
    food_description: Optional[str] = None
    calories: Optional[float] = Field(None, ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    fiber_g: Optional[float] = Field(None, ge=0)
    sodium_mg: Optional[float] = Field(None, ge=0)
    portion_size: Optional[str] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None


class DietRecordResponse(DietRecordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Daily Nutrition Summary Schema
class DailyNutritionSummary(BaseModel):
    date: datetime
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    total_sodium_mg: float
    meal_count: int
