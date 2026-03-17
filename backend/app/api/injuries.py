from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.schemas.injury import InjuryRecordCreate, InjuryRecordUpdate, InjuryRecordResponse
from app.services.injury_service import InjuryService
from app.core.dependencies import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[InjuryRecordResponse])
async def list_injuries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ongoing_only: bool = Query(False),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all injury records for current user"""
    injury_service = InjuryService(db)
    injuries = await injury_service.get_all_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        ongoing_only=ongoing_only
    )
    return injuries


@router.post("/", response_model=InjuryRecordResponse, status_code=201)
async def create_injury(
    injury_data: InjuryRecordCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new injury record"""
    injury_service = InjuryService(db)
    injury = await injury_service.create(current_user.id, injury_data)
    return injury


@router.get("/{injury_id}", response_model=InjuryRecordResponse)
async def get_injury(
    injury_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific injury record"""
    injury_service = InjuryService(db)
    injury = await injury_service.get_by_id(injury_id, current_user.id)
    if not injury:
        raise HTTPException(status_code=404, detail="Injury record not found")
    return injury


@router.put("/{injury_id}", response_model=InjuryRecordResponse)
async def update_injury(
    injury_id: int,
    injury_data: InjuryRecordUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an injury record"""
    injury_service = InjuryService(db)
    injury = await injury_service.update(injury_id, current_user.id, injury_data)
    return injury


@router.delete("/{injury_id}")
async def delete_injury(
    injury_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an injury record"""
    injury_service = InjuryService(db)
    await injury_service.delete(injury_id, current_user.id)
    return {"message": "Injury record deleted successfully"}


@router.get("/summary/statistics")
async def get_injury_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get injury statistics summary for current user"""
    injury_service = InjuryService(db)
    summary = await injury_service.get_injury_summary(current_user.id)
    return summary
