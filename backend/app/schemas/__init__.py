from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserProfileCreate, UserProfileUpdate, UserProfileResponse
from app.schemas.auth import LoginRequest, LoginResponse, TokenRefreshRequest
from app.schemas.injury import InjuryRecordCreate, InjuryRecordUpdate, InjuryRecordResponse
from app.schemas.sport import (
    SportRecordCreate, SportRecordUpdate, SportRecordResponse,
    RunningDetailCreate, RunningDetailResponse,
    BadmintonDetailCreate, BadmintonDetailResponse
)
from app.schemas.diet import DietRecordCreate, DietRecordUpdate, DietRecordResponse
from app.schemas.strength import StrengthRecordCreate, StrengthRecordUpdate, StrengthRecordResponse

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse",
    "UserProfileCreate", "UserProfileUpdate", "UserProfileResponse",
    "LoginRequest", "LoginResponse", "TokenRefreshRequest",
    "InjuryRecordCreate", "InjuryRecordUpdate", "InjuryRecordResponse",
    "SportRecordCreate", "SportRecordUpdate", "SportRecordResponse",
    "RunningDetailCreate", "RunningDetailResponse",
    "BadmintonDetailCreate", "BadmintonDetailResponse",
    "DietRecordCreate", "DietRecordUpdate", "DietRecordResponse",
    "StrengthRecordCreate", "StrengthRecordUpdate", "StrengthRecordResponse",
]
