from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class InjuryRecordBase(BaseModel):
    injury_type: str = Field(..., description="Type of injury: strain, sprain, inflammation, etc.")
    body_part: str = Field(..., description="Body part affected: knee, ankle, shoulder, etc.")
    severity: str = Field(..., description="Severity: mild, moderate, severe")
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    treatment: Optional[str] = None
    is_recurring: bool = False
    is_ongoing: bool = True


class InjuryRecordCreate(InjuryRecordBase):
    pass


class InjuryRecordUpdate(BaseModel):
    injury_type: Optional[str] = None
    body_part: Optional[str] = None
    severity: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    treatment: Optional[str] = None
    is_recurring: Optional[bool] = None
    is_ongoing: Optional[bool] = None


class InjuryRecordResponse(InjuryRecordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
