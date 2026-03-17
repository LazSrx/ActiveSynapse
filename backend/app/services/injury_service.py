from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.injury import InjuryRecord
from app.schemas.injury import InjuryRecordCreate, InjuryRecordUpdate
from app.core.exceptions import NotFoundError


class InjuryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, injury_id: int, user_id: int) -> Optional[InjuryRecord]:
        """Get injury record by ID and verify ownership"""
        result = await self.db.execute(
            select(InjuryRecord)
            .where(InjuryRecord.id == injury_id)
            .where(InjuryRecord.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        ongoing_only: bool = False
    ) -> List[InjuryRecord]:
        """Get all injury records for a user"""
        query = select(InjuryRecord).where(InjuryRecord.user_id == user_id)

        if ongoing_only:
            query = query.where(InjuryRecord.is_ongoing == True)

        query = query.order_by(desc(InjuryRecord.start_date)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, user_id: int, injury_data: InjuryRecordCreate) -> InjuryRecord:
        """Create a new injury record"""
        db_injury = InjuryRecord(
            user_id=user_id,
            injury_type=injury_data.injury_type,
            body_part=injury_data.body_part,
            severity=injury_data.severity,
            start_date=injury_data.start_date,
            end_date=injury_data.end_date,
            description=injury_data.description,
            treatment=injury_data.treatment,
            is_recurring=injury_data.is_recurring,
            is_ongoing=injury_data.is_ongoing
        )
        self.db.add(db_injury)
        await self.db.commit()
        await self.db.refresh(db_injury)
        return db_injury

    async def update(
        self,
        injury_id: int,
        user_id: int,
        injury_data: InjuryRecordUpdate
    ) -> InjuryRecord:
        """Update an injury record"""
        injury = await self.get_by_id(injury_id, user_id)
        if not injury:
            raise NotFoundError("Injury record not found")

        update_data = injury_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(injury, field, value)

        await self.db.commit()
        await self.db.refresh(injury)
        return injury

    async def delete(self, injury_id: int, user_id: int) -> bool:
        """Delete an injury record"""
        injury = await self.get_by_id(injury_id, user_id)
        if not injury:
            raise NotFoundError("Injury record not found")

        await self.db.delete(injury)
        await self.db.commit()
        return True

    async def get_injury_summary(self, user_id: int) -> dict:
        """Get injury summary statistics for a user"""
        result = await self.db.execute(
            select(InjuryRecord).where(InjuryRecord.user_id == user_id)
        )
        injuries = result.scalars().all()

        total_injuries = len(injuries)
        ongoing_injuries = sum(1 for i in injuries if i.is_ongoing)
        recurring_injuries = sum(1 for i in injuries if i.is_recurring)

        # Count by body part
        body_part_counts = {}
        for injury in injuries:
            body_part_counts[injury.body_part] = body_part_counts.get(injury.body_part, 0) + 1

        # Count by type
        type_counts = {}
        for injury in injuries:
            type_counts[injury.injury_type] = type_counts.get(injury.injury_type, 0) + 1

        return {
            "total_injuries": total_injuries,
            "ongoing_injuries": ongoing_injuries,
            "recurring_injuries": recurring_injuries,
            "body_part_distribution": body_part_counts,
            "injury_type_distribution": type_counts
        }
