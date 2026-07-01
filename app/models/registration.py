from datetime import datetime, timezone

from app.extensions import db
from app.domain.value_objects import CheckInStatus, DateTime, RegistrationStatus
from sqlalchemy.ext.hybrid import hybrid_property


class Registration(db.Model):
    __tablename__ = "registrations"

    registration_id = db.Column(db.Integer, primary_key=True)
    _registration_time = db.Column("registration_time", db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    _registration_status = db.Column("registration_status", db.String(30), nullable=False, default="Pending")
    _check_in_status = db.Column("check_in_status", db.String(30), nullable=False, default="NotCheckedIn")
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("music_events.event_id"), nullable=False)

    participant = db.relationship("Participant", back_populates="registrations")
    music_event = db.relationship("MusicEvent", back_populates="registrations")
    ticket = db.relationship("Ticket", back_populates="registration", uselist=False)
    payment = db.relationship("Payment", back_populates="registration", uselist=False)

    @hybrid_property
    def registration_time(self) -> DateTime:
        return DateTime(self._registration_time)

    @registration_time.expression
    def registration_time(cls):
        return cls._registration_time

    @registration_time.setter
    def registration_time(self, value: DateTime) -> None:
        if not isinstance(value, DateTime):
            raise TypeError("registration_time must be a DateTime value object")
        self._registration_time = value.value

    @hybrid_property
    def registration_status(self) -> RegistrationStatus:
        return RegistrationStatus(self._registration_status or "Pending")

    @registration_status.expression
    def registration_status(cls):
        return cls._registration_status

    @registration_status.setter
    def registration_status(self, value: RegistrationStatus) -> None:
        if not isinstance(value, RegistrationStatus):
            raise TypeError("registration_status must be a RegistrationStatus value object")
        self._registration_status = value.value

    @hybrid_property
    def check_in_status(self) -> CheckInStatus:
        return CheckInStatus(self._check_in_status or "NotCheckedIn")

    @check_in_status.expression
    def check_in_status(cls):
        return cls._check_in_status

    @check_in_status.setter
    def check_in_status(self, value: CheckInStatus) -> None:
        if not isinstance(value, CheckInStatus):
            raise TypeError("check_in_status must be a CheckInStatus value object")
        self._check_in_status = value.value

    def confirmRegistration(self) -> bool:
        self.registration_status = RegistrationStatus("Confirmed")
        db.session.commit()
        return True

    def cancelRegistration(self) -> bool:
        self.registration_status = RegistrationStatus("Cancelled")
        db.session.commit()
        return True

    def markCheckedIn(self) -> bool:
        self.check_in_status = CheckInStatus("CheckedIn")
        db.session.commit()
        return True
