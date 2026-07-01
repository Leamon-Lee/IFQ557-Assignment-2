from datetime import datetime, timezone

from app.extensions import db


class Announcement(db.Model):
    __tablename__ = "announcements"

    announcement_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    event_id = db.Column(db.Integer, db.ForeignKey("music_events.event_id"), nullable=False)

    music_event = db.relationship("MusicEvent", back_populates="announcements")
