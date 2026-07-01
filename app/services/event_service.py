from app.extensions import db
from app.models.music_event import MusicEvent
from app.models.registration import Registration


class EventService:
    def listEvents(self, genre: str | None = None):
        """获取活动列表，可选按分类筛选。返回按 start_time 升序排列。"""
        query = MusicEvent.query
        if genre:
            query = query.filter_by(music_genre=genre)
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