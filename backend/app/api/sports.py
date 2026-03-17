from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.schemas.sport import SportRecordCreate, SportRecordUpdate, SportRecordResponse, SportStatistics
from app.services.sport_service import SportService
from app.core.dependencies import get_current_active_user

router = APIRouter()


@router.get("/records", response_model=List[SportRecordResponse])
async def list_sport_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sport_type: Optional[str] = Query(None, description="Filter by sport type: running, badminton"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all sport records for current user with optional filters"""
    sport_service = SportService(db)
    records = await sport_service.get_all_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        sport_type=sport_type,
        start_date=start_date,
        end_date=end_date
    )
    return records


@router.post("/records", response_model=SportRecordResponse, status_code=201)
async def create_sport_record(
    record_data: SportRecordCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new sport record"""
    sport_service = SportService(db)
    record = await sport_service.create(current_user.id, record_data)
    return record


@router.get("/records/{record_id}", response_model=SportRecordResponse)
async def get_sport_record(
    record_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific sport record"""
    sport_service = SportService(db)
    record = await sport_service.get_by_id(record_id, current_user.id)
    if not record:
        raise HTTPException(status_code=404, detail="Sport record not found")
    return record


@router.put("/records/{record_id}", response_model=SportRecordResponse)
async def update_sport_record(
    record_id: int,
    record_data: SportRecordUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a sport record"""
    sport_service = SportService(db)
    record = await sport_service.update(record_id, current_user.id, record_data)
    return record


@router.delete("/records/{record_id}")
async def delete_sport_record(
    record_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a sport record"""
    sport_service = SportService(db)
    await sport_service.delete(record_id, current_user.id)
    return {"message": "Sport record deleted successfully"}


@router.get("/statistics", response_model=dict)
async def get_sport_statistics(
    sport_type: Optional[str] = Query(None, description="Filter by sport type: running, badminton"),
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get sport statistics for current user"""
    sport_service = SportService(db)
    stats = await sport_service.get_statistics(
        user_id=current_user.id,
        sport_type=sport_type,
        days=days
    )
    return stats


@router.get("/weekly-summary", response_model=dict)
async def get_weekly_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get weekly activity summary"""
    sport_service = SportService(db)
    summary = await sport_service.get_weekly_summary(current_user.id)
    return summary


@router.post("/records/import")
async def import_gpx_file(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Import GPX file from COROS (placeholder - implement actual file upload)"""
    # TODO: Implement GPX file upload and parsing
    return {
        "message": "GPX import endpoint - implement with file upload",
        "user_id": current_user.id
    }
