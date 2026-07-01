from app.domain.value_objects import CheckInStatus, RegistrationStatus
from app.extensions import db


class Registration(db.Model):
    __tablename__ = "registrations"

    registration_id = db.Column(db.Integer, primary_key=True)
    registration_time = db.Column(db.DateTime, nullable=False)
    _registration_status = db.Column("registration_status", db.String(30), nullable=False)
    _check_in_status = db.Column("check_in_status", db.String(30), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("music_events.event_id"), nullable=False)

    participant = db.relationship("Participant", back_populates="registrations")
    music_event = db.relationship("MusicEvent", back_populates="registrations")
    ticket = db.relationship("Ticket", back_populates="registration", uselist=False)
    payment = db.relationship("Payment", back_populates="registration", uselist=False)

    @property
    def registration_status(self) -> RegistrationStatus:
        return RegistrationStatus(self._registration_status)

    @registration_status.setter
    def registration_status(self, value: RegistrationStatus | str) -> None:
        registration_status = value if isinstance(value, RegistrationStatus) else RegistrationStatus(value)
        self._registration_status = registration_status.value

    @property
    def check_in_status(self) -> CheckInStatus:
        return CheckInStatus(self._check_in_status)

    @check_in_status.setter
    def check_in_status(self, value: CheckInStatus | str) -> None:
        check_in_status = value if isinstance(value, CheckInStatus) else CheckInStatus(value)
        self._check_in_status = check_in_status.value

    def confirmRegistration(self) -> bool:
        return

    def cancelRegistration(self) -> bool:
        return

    def markCheckedIn(self) -> bool:
        return
