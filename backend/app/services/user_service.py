from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate, UserProfileCreate, UserProfileUpdate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import NotFoundError, ConflictError


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email exists
        existing_email = await self.get_by_email(user_data.email)
        if existing_email:
            raise ConflictError("Email already registered")

        # Check if username exists
        existing_username = await self.get_by_username(user_data.username)
        if existing_username:
            raise ConflictError("Username already taken")

        # Create user
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            phone=user_data.phone,
            is_active=True,
            is_verified=False
        )
        self.db.add(db_user)
        await self.db.flush()

        # Create empty profile
        profile = UserProfile(user_id=db_user.id)
        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user information"""
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        update_data = user_data.model_dump(exclude_unset=True)

        # Check email uniqueness if updating email
        if "email" in update_data:
            existing = await self.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise ConflictError("Email already registered")

        # Check username uniqueness if updating username
        if "username" in update_data:
            existing = await self.get_by_username(update_data["username"])
            if existing and existing.id != user_id:
                raise ConflictError("Username already taken")

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_profile(self, user_id: int) -> Optional[UserProfile]:
        """Get user profile"""
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_profile(self, user_id: int, profile_data: UserProfileUpdate) -> UserProfile:
        """Update or create user profile"""
        profile = await self.get_profile(user_id)

        if not profile:
            # Create new profile
            profile = UserProfile(user_id=user_id)
            self.db.add(profile)

        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

        await self.db.commit()
        await self.db.refresh(profile)
        return profile
