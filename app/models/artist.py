from app.extensions import db
from app.models.music_event import event_artist


class Artist(db.Model):
    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    second_name = db.Column(db.String(80), nullable=False)
    artist_type = db.Column(db.String(80), nullable=False)
    music_genre = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(100))

    events = db.relationship("MusicEvent", secondary=event_artist, back_populates="artists")

    def updateProfile(self, first_name: str, second_name: str, bio: str) -> bool:
        self.first_name = first_name
        self.second_name = second_name
        self.bio = bio
        db.session.commit()
        return True

    def viewEvents(self) -> list:
        return [event.event_id for event in self.events]
