from app.extensions import db
from app.models.user import User


class Participant(User):
    __tablename__ = "participants"

    participant_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    second_name = db.Column(db.String(80), nullable=False)

    registrations = db.relationship("Registration", back_populates="participant")

    __mapper_args__ = {
        "polymorphic_identity": "participant",
    }

    def browseEvents(self) -> list:
        return

    def registerEvent(self, event_id: int) -> int:
        return

    def cancelRegistration(self, registration_id: int) -> bool:
        return

    def viewTicket(self, ticket_id: int) -> object:
        return

    def checkIn(self, ticket_id: int) -> bool:
        return
