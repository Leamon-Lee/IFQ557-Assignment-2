from app.extensions import db
from app.models.user import User


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

    def createEvent(self) -> int:
        return

    def updateEvent(self, event_id: int) -> bool:
        return

    def cancelEvent(self, event_id: int) -> bool:
        return

    def viewParticipants(self, event_id: int) -> list:
        return

    def sendAnnouncement(self, event_id: int, message: str) -> bool:
        return
