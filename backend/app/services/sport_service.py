from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, and_
from app.models.sport import SportRecord, RunningDetail, BadmintonDetail
from app.schemas.sport import SportRecordCreate, SportRecordUpdate, RunningDetailCreate, BadmintonDetailCreate
from app.core.exceptions import NotFoundError


class SportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, record_id: int, user_id: int) -> Optional[SportRecord]:
        """Get sport record by ID and verify ownership"""
        result = await self.db.execute(
            select(SportRecord)
            .where(SportRecord.id == record_id)
            .where(SportRecord.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        sport_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[SportRecord]:
        """Get all sport records for a user with optional filters"""
        query = select(SportRecord).where(SportRecord.user_id == user_id)

        if sport_type:
            query = query.where(SportRecord.sport_type == sport_type)

        if start_date:
            query = query.where(SportRecord.record_date >= start_date)

        if end_date:
            query = query.where(SportRecord.record_date <= end_date)

        query = query.order_by(desc(SportRecord.record_date)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, user_id: int, record_data: SportRecordCreate) -> SportRecord:
        """Create a new sport record with details"""
        # Create main record
        db_record = SportRecord(
            user_id=user_id,
            sport_type=record_data.sport_type,
            record_date=record_data.record_date,
            duration_minutes=record_data.duration_minutes,
            calories_burned=record_data.calories_burned,
            notes=record_data.notes,
            source=record_data.source,
            gpx_file_url=record_data.gpx_file_url
        )
        self.db.add(db_record)
        await self.db.flush()  # Flush to get the record ID

        # Create detail records based on sport type
        if record_data.sport_type == "running" and record_data.running_detail:
            running_detail = RunningDetail(
                record_id=db_record.id,
                distance_km=record_data.running_detail.distance_km,
                pace_min_per_km=record_data.running_detail.pace_min_per_km,
                heart_rate_avg=record_data.running_detail.heart_rate_avg,
                heart_rate_max=record_data.running_detail.heart_rate_max,
                elevation_gain_m=record_data.running_detail.elevation_gain_m,
                elevation_loss_m=record_data.running_detail.elevation_loss_m,
                cadence_avg=record_data.running_detail.cadence_avg,
                stride_length_cm=record_data.running_detail.stride_length_cm,
                weather_conditions=record_data.running_detail.weather_conditions,
                route_data=record_data.running_detail.route_data
            )
            self.db.add(running_detail)

        elif record_data.sport_type == "badminton" and record_data.badminton_detail:
            badminton_detail = BadmintonDetail(
                record_id=db_record.id,
                match_type=record_data.badminton_detail.match_type,
                opponent_level=record_data.badminton_detail.opponent_level,
                score=record_data.badminton_detail.score,
                court_type=record_data.badminton_detail.court_type,
                video_url=record_data.badminton_detail.video_url,
                highlights=record_data.badminton_detail.highlights,
                stats=record_data.badminton_detail.stats
            )
            self.db.add(badminton_detail)

        await self.db.commit()
        await self.db.refresh(db_record)
        return db_record

    async def update(
        self,
        record_id: int,
        user_id: int,
        record_data: SportRecordUpdate
    ) -> SportRecord:
        """Update a sport record"""
        record = await self.get_by_id(record_id, user_id)
        if not record:
            raise NotFoundError("Sport record not found")

        update_data = record_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)

        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def delete(self, record_id: int, user_id: int) -> bool:
        """Delete a sport record"""
        record = await self.get_by_id(record_id, user_id)
        if not record:
            raise NotFoundError("Sport record not found")

        await self.db.delete(record)
        await self.db.commit()
        return True

    async def get_statistics(
        self,
        user_id: int,
        sport_type: Optional[str] = None,
        days: int = 30
    ) -> dict:
        """Get sport statistics for a user"""
        start_date = datetime.utcnow() - timedelta(days=days)

        query = select(SportRecord).where(
            and_(
                SportRecord.user_id == user_id,
                SportRecord.record_date >= start_date
            )
        )

        if sport_type:
            query = query.where(SportRecord.sport_type == sport_type)

        result = await self.db.execute(query)
        records = result.scalars().all()

        total_activities = len(records)
        total_duration = sum(r.duration_minutes for r in records)
        total_calories = sum(r.calories_burned or 0 for r in records)

        avg_duration = total_duration / total_activities if total_activities > 0 else 0

        stats = {
            "total_activities": total_activities,
            "total_duration_minutes": total_duration,
            "total_calories": total_calories,
            "avg_duration_minutes": round(avg_duration, 2),
            "period_days": days
        }

        # Add running-specific stats
        if sport_type == "running" or sport_type is None:
            running_records = [r for r in records if r.sport_type == "running"]
            if running_records:
                # Get running details
                record_ids = [r.id for r in running_records]
                running_result = await self.db.execute(
                    select(RunningDetail).where(RunningDetail.record_id.in_(record_ids))
                )
                running_details = running_result.scalars().all()

                total_distance = sum(d.distance_km for d in running_details)
                avg_pace = sum(d.pace_min_per_km or 0 for d in running_details) / len(running_details) if running_details else 0
                avg_hr = sum(d.heart_rate_avg or 0 for d in running_details) / len(running_details) if running_details else 0

                stats["running"] = {
                    "total_distance_km": round(total_distance, 2),
                    "avg_pace_min_per_km": round(avg_pace, 2) if avg_pace > 0 else None,
                    "avg_heart_rate": round(avg_hr) if avg_hr > 0 else None
                }

        # Add badminton-specific stats
        if sport_type == "badminton" or sport_type is None:
            badminton_records = [r for r in records if r.sport_type == "badminton"]
            if badminton_records:
                stats["badminton"] = {
                    "total_sessions": len(badminton_records),
                    "total_duration_minutes": sum(r.duration_minutes for r in badminton_records)
                }

        return stats

    async def get_weekly_summary(self, user_id: int) -> dict:
        """Get weekly activity summary"""
        # Get data for the last 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)

        result = await self.db.execute(
            select(SportRecord)
            .where(SportRecord.user_id == user_id)
            .where(SportRecord.record_date >= start_date)
            .order_by(SportRecord.record_date)
        )
        records = result.scalars().all()

        # Group by day
        daily_stats = {}
        for i in range(7):
            day = (end_date - timedelta(days=i)).date()
            daily_stats[day.isoformat()] = {
                "running_minutes": 0,
                "badminton_minutes": 0,
                "other_minutes": 0,
                "total_calories": 0
            }

        for record in records:
            day = record.record_date.date().isoformat()
            if day in daily_stats:
                if record.sport_type == "running":
                    daily_stats[day]["running_minutes"] += record.duration_minutes
                elif record.sport_type == "badminton":
                    daily_stats[day]["badminton_minutes"] += record.duration_minutes
                else:
                    daily_stats[day]["other_minutes"] += record.duration_minutes

                daily_stats[day]["total_calories"] += record.calories_burned or 0

        return {
            "week_start": start_date.date().isoformat(),
            "week_end": end_date.date().isoformat(),
            "daily_breakdown": daily_stats,
            "total_activities": len(records)
        }
