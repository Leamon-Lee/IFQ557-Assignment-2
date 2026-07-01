from app.extensions import db


class Registration(db.Model):
    __tablename__ = "registrations"

    registration_id = db.Column(db.Integer, primary_key=True)
    registration_time = db.Column(db.DateTime, nullable=False)
    registration_status = db.Column(db.String(30), nullable=False)
    check_in_status = db.Column(db.String(30), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("music_events.event_id"), nullable=False)

    participant = db.relationship("Participant", back_populates="registrations")
    music_event = db.relationship("MusicEvent", back_populates="registrations")
    ticket = db.relationship("Ticket", back_populates="registration", uselist=False)
    payment = db.relationship("Payment", back_populates="registration", uselist=False)

    def confirmRegistration(self) -> bool:
        return

    def cancelRegistration(self) -> bool:
        return

    def markCheckedIn(self) -> bool:
        return
