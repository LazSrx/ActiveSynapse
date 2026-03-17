from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings
from app.schemas.auth import LoginRequest, LoginResponse, TokenRefreshRequest, UserInfo
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token, decode_token, verify_password
from app.core.exceptions import AuthenticationError, ValidationError

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    user_service = UserService(db)
    user = await user_service.create(user_data)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login user and return tokens"""
    user_service = UserService(db)
    user = await user_service.authenticate(login_data.email, login_data.password)

    if not user:
        raise AuthenticationError("Invalid email or password")

    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url
        )
    )


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(refresh_data: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    """Refresh access token using refresh token"""
    payload = decode_token(refresh_data.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise AuthenticationError("Invalid refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid token payload")

    user_service = UserService(db)
    user = await user_service.get_by_id(int(user_id))

    if not user or not user.is_active:
        raise AuthenticationError("User not found or inactive")

    # Create new tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url
        )
    )


@router.post("/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}
