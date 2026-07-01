from datetime import datetime, timezone

from app.extensions import db


class Registration(db.Model):
    __tablename__ = "registrations"

    registration_id = db.Column(db.Integer, primary_key=True)
    registration_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    registration_status = db.Column(db.String(30), nullable=False, default="Pending")
    check_in_status = db.Column(db.String(30), nullable=False, default="NotCheckedIn")
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("music_events.event_id"), nullable=False)

    participant = db.relationship("Participant", back_populates="registrations")
    music_event = db.relationship("MusicEvent", back_populates="registrations")
    ticket = db.relationship("Ticket", back_populates="registration", uselist=False)
    payment = db.relationship("Payment", back_populates="registration", uselist=False)

    def confirmRegistration(self) -> bool:
        self.registration_status = "Confirmed"
        db.session.commit()
        return True

    def cancelRegistration(self) -> bool:
        self.registration_status = "Cancelled"
        db.session.commit()
        return True

    def markCheckedIn(self) -> bool:
        self.check_in_status = "CheckedIn"
        db.session.commit()
        return True
