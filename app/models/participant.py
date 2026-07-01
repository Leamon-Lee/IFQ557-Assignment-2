from app.extensions import db
from .user import User


class Participant(User):
    __tablename__ = "participants"

    participant_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    _first_name = db.Column("first_name", db.String(30), nullable=False)
    _second_name = db.Column("second_name", db.String(30), nullable=False)

    registrations = db.relationship("Registration", back_populates="participant")

    __mapper_args__ = {
        "polymorphic_identity": "participant",
    }

    @property
    def first_name(self) -> Name:
        return Name(self._first_name)

    @first_name.setter
    def first_name(self, value: Name) -> None:
        if not isinstance(value, Name):
            raise TypeError("first_name must be a Name value object")
        self._first_name = value.value

    @property
    def second_name(self) -> Name:
        return Name(self._second_name)

    @second_name.setter
    def second_name(self, value: Name) -> None:
        if not isinstance(value, Name):
            raise TypeError("second_name must be a Name value object")
        self._second_name = value.value

    def browseEvents(self) -> list:
        from app.models.music_event import MusicEvent
        return MusicEvent.query.all()

    def registerEvent(self, event_id: int) -> int:
        from app.models.registration import Registration
        new_reg = Registration(participant_id=self.participant_id, event_id=event_id)
        db.session.add(new_reg)
        db.session.commit()
        return new_reg.registration_id

    def cancelRegistration(self, registration_id: int) -> bool:
        from app.models.registration import Registration
        reg = Registration.query.filter_by(registration_id=registration_id, participant_id=self.participant_id).first()
        if reg:
            reg.registration_status = "Cancelled"
            db.session.commit()
            return True
        return False

    def viewTicket(self, ticket_id: int) -> object:
        from app.models.ticket import Ticket
        return Ticket.query.get(ticket_id)

    def checkIn(self, ticket_id: int) -> bool:
        return True
