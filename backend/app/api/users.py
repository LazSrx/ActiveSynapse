from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserProfileResponse, UserProfileUpdate
from app.services.user_service import UserService
from app.core.dependencies import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information"""
    # Load profile
    user_service = UserService(db)
    profile = await user_service.get_profile(current_user.id)

    # Convert to response model
    user_dict = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "avatar_url": current_user.avatar_url,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
        "profile": profile if profile else None
    }
    return UserResponse.model_validate(user_dict)


@router.put("/me", response_model=UserResponse)
async def update_user_info(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user information"""
    user_service = UserService(db)
    updated_user = await user_service.update(current_user.id, user_data)
    return updated_user


@router.get("/me/profile", response_model=Optional[UserProfileResponse])
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile"""
    user_service = UserService(db)
    profile = await user_service.get_profile(current_user.id)
    return profile


@router.put("/me/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update or create user profile"""
    user_service = UserService(db)
    profile = await user_service.update_profile(current_user.id, profile_data)
    return profile


@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload user avatar (placeholder - implement with actual storage)"""
    # TODO: Implement actual file upload to storage service
    # For now, return a placeholder response
    return {
        "message": "Avatar upload endpoint - implement with storage service",
        "filename": file.filename,
        "content_type": file.content_type
    }
