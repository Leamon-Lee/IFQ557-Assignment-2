from app.extensions import db


class Venue(db.Model):
    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    room = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    events = db.relationship("MusicEvent", back_populates="venue")

    def checkAvailability(self, start_time, end_time) -> bool:
        from app.models.music_event import MusicEvent
        conflicting_events = MusicEvent.query.filter(
            MusicEvent.venue_id == self.venue_id,
            MusicEvent.start_time < end_time,
            MusicEvent.end_time > start_time
        ).count()

        return conflicting_events == 0