from werkzeug.security import generate_password_hash

from app.extensions import db


class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def reviewEvent(self, event_id: int, status: str) -> bool:
        from app.models.music_event import MusicEvent
        event = MusicEvent.query.get(event_id)
        if event:
            event.event_status = status
            db.session.commit()
            return True
        return False

    def approveEvent(self, event_id: int) -> bool:
        return self.reviewEvent(event_id, "Open")

    def rejectEvent(self, event_id: int) -> bool:
        return self.reviewEvent(event_id, "Cancelled")

    def manageUsers(self, user_id: int) -> bool:
        return True

    def generateReport(self) -> str:
        from app.models.music_event import MusicEvent
        count = MusicEvent.query.count()
        return f"Total events in system: {count}"
