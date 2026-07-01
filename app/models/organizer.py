from app.extensions import db
from .user import User


class Organizer(User):
    __tablename__ = "organizers"

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    organization_name = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    second_name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(100))

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
            organizer_id=self.organizer_id
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
