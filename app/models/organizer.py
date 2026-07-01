from app.extensions import db
from .user import User


class Organizer(User):
    __tablename__ = "organizers"

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    _organization_name = db.Column("organization_name", db.String(120), nullable=False)
    _first_name = db.Column("first_name", db.String(30), nullable=False)
    _second_name = db.Column("second_name", db.String(30), nullable=False)
    _bio = db.Column("bio", db.String(100))

    events = db.relationship("MusicEvent", back_populates="organizer")

    __mapper_args__ = {
        "polymorphic_identity": "organizer",
    }

    def createEvent(self, title, description, start_time, end_time, capacity) -> int:
        from app.models.music_event import MusicEvent
        new_event = MusicEvent(
            event_title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            age_restriction=0,
            event_status="Open",
            music_genre="General",
            organizer_id=self.organizer_id,
            venue_id=1,
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event.event_id

    def updateEvent(self, event_id: int, **kwargs) -> bool:
        from app.models.music_event import MusicEvent
        event = MusicEvent.query.filter_by(event_id=event_id, organizer_id=self.organizer_id).first()
        if event:
            for key, value in kwargs.items():
                setattr(event, key, value)
            db.session.commit()
            return True
        return False

    def cancelEvent(self, event_id: int) -> bool:
        from app.models.music_event import MusicEvent
        event = MusicEvent.query.filter_by(event_id=event_id, organizer_id=self.organizer_id).first()
        if event:
            event.event_status = "Cancelled"
            db.session.commit()
            return True
        return False

    def viewParticipants(self, event_id: int) -> list:
        from app.models.registration import Registration
        return Registration.query.filter_by(event_id=event_id).all()

    def sendAnnouncement(self, event_id: int, message: str) -> bool:
        return True
