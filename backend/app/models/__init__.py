from app.models.user import User, UserProfile
from app.models.injury import InjuryRecord
from app.models.sport import SportRecord, RunningDetail, BadmintonDetail
from app.models.diet import DietRecord
from app.models.strength import StrengthTrainingRecord
from app.models.ai import AISuggestion, TrainingPlan

__all__ = [
    "User",
    "UserProfile",
    "InjuryRecord",
    "SportRecord",
    "RunningDetail",
    "BadmintonDetail",
    "DietRecord",
    "StrengthTrainingRecord",
    "AISuggestion",
    "TrainingPlan",
]
