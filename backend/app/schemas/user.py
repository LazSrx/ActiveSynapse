from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# User Profile Schemas
class UserProfileBase(BaseModel):
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    sport_level: Optional[str] = None  # beginner/intermediate/advanced
    sport_goals: Optional[List[str]] = Field(default_factory=list)
    preferred_sports: Optional[List[str]] = Field(default_factory=list)
    weekly_target: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True


class UserWithProfile(UserResponse):
    profile: Optional[UserProfileResponse] = None
