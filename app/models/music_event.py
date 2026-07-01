from app.extensions import db


event_artist = db.Table(
    "event_artist",
    db.Column("event_id", db.Integer, db.ForeignKey("music_events.event_id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.artist_id"), primary_key=True),
)


class MusicEvent(db.Model):
    __tablename__ = "music_events"

    event_id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    age_restriction = db.Column(db.Integer, nullable=False)
    event_status = db.Column(db.String(30), nullable=False, default="Open")
    music_genre = db.Column(db.String(80), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizers.organizer_id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.venue_id"), nullable=False)

    organizer = db.relationship("Organizer", back_populates="events")
    venue = db.relationship("Venue", back_populates="events")
    artists = db.relationship("Artist", secondary=event_artist, back_populates="events")
    registrations = db.relationship("Registration", back_populates="music_event")

    def publish(self) -> bool:
        self.event_status = "Open"
        db.session.commit()
        return True

    def cancel(self) -> bool:
        self.event_status = "Cancelled"
        db.session.commit()
        return True

    def updateInfo(self, event_title: str, description: str, start_time: object, end_time: object) -> bool:
        self.event_title = event_title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        db.session.commit()
        return True

    def isFull(self) -> bool:
        return len(self.registrations) >= self.capacity
