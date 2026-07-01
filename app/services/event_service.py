from datetime import datetime, timedelta

from sqlalchemy import or_

from app.extensions import db
from app.models.artist import Artist
from app.models.music_event import MusicEvent
from app.models.registration import Registration
from app.models.venue import Venue


class EventService:
    def listEvents(self, genre: str | None = None, search: str | None = None, date_filter: str | None = None):
        query = MusicEvent.query
        if genre:
            query = query.filter_by(music_genre=genre)
        if search:
            pattern = f"%{search}%"
            query = query.outerjoin(Venue).outerjoin(
                Artist, MusicEvent.artists
            ).filter(
                or_(
                    MusicEvent.event_title.ilike(pattern),
                    Venue.venue_name.ilike(pattern),
                    Artist.first_name.ilike(pattern),
                    Artist.second_name.ilike(pattern),
                )
            ).distinct()
        if date_filter == "week":
            today = datetime.now()
            week_end = today + timedelta(days=7)
            query = query.filter(MusicEvent.start_time >= today, MusicEvent.start_time <= week_end)
        elif date_filter == "month":
            today = datetime.now()
            month_end = today + timedelta(days=30)
            query = query.filter(MusicEvent.start_time >= today, MusicEvent.start_time <= month_end)
        return query.order_by(MusicEvent.start_time.asc()).all()

    def getEvent(self, event_id: int):
        """获取单个活动详情，找不到返回 None。"""
        return db.session.get(MusicEvent, event_id)

    def getConfirmedCount(self, event_id: int) -> int:
        """统计某个活动的已确认报名人数。"""
        return Registration.query.filter_by(
            event_id=event_id, registration_status="Confirmed"
        ).count()

    def getRemainingTickets(self, event_id: int) -> int:
        """计算剩余票数 = 容量 - 已确认报名数。"""
        event = self.getEvent(event_id)
        if not event:
            return 0
        confirmed = self.getConfirmedCount(event_id)
        return max(event.capacity - confirmed, 0)