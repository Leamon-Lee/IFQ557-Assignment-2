from app.domain.value_objects import AgeRestriction, Capacity, EventStatus, EventTitle, MusicGenre, Text200
from app.extensions import db


event_artist = db.Table(
    "event_artist",
    db.Column("event_id", db.Integer, db.ForeignKey("music_events.event_id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.artist_id"), primary_key=True),
)


class MusicEvent(db.Model):
    __tablename__ = "music_events"

    event_id = db.Column(db.Integer, primary_key=True)
    _event_title = db.Column("event_title", db.String(100), nullable=False)
    _description = db.Column("description", db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    _capacity = db.Column("capacity", db.Integer, nullable=False)
    _age_restriction = db.Column("age_restriction", db.Integer, nullable=False)
    _event_status = db.Column("event_status", db.String(30), nullable=False, default="draft")
    _music_genre = db.Column("music_genre", db.String(80), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizers.organizer_id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.venue_id"), nullable=False)

    organizer = db.relationship("Organizer", back_populates="events")
    venue = db.relationship("Venue", back_populates="events")
    artists = db.relationship("Artist", secondary=event_artist, back_populates="events")
    registrations = db.relationship("Registration", back_populates="music_event")

    @property
    def event_title(self) -> EventTitle:
        return EventTitle(self._event_title)

    @event_title.setter
    def event_title(self, value: EventTitle | str) -> None:
        event_title = value if isinstance(value, EventTitle) else EventTitle(value)
        self._event_title = event_title.value

    @property
    def description(self) -> Text200:
        return Text200(self._description)

    @description.setter
    def description(self, value: Text200 | str) -> None:
        description = value if isinstance(value, Text200) else Text200(value)
        self._description = description.value

    @property
    def capacity(self) -> Capacity:
        return Capacity(self._capacity)

    @capacity.setter
    def capacity(self, value: Capacity | int) -> None:
        capacity = value if isinstance(value, Capacity) else Capacity(value)
        self._capacity = capacity.value

    @property
    def age_restriction(self) -> AgeRestriction:
        return AgeRestriction(self._age_restriction)

    @age_restriction.setter
    def age_restriction(self, value: AgeRestriction | int) -> None:
        age_restriction = value if isinstance(value, AgeRestriction) else AgeRestriction(value)
        self._age_restriction = age_restriction.value

    @property
    def event_status(self) -> EventStatus:
        return EventStatus(self._event_status)

    @event_status.setter
    def event_status(self, value: EventStatus | str) -> None:
        event_status = value if isinstance(value, EventStatus) else EventStatus(value)
        self._event_status = event_status.value

    @property
    def music_genre(self) -> MusicGenre:
        return MusicGenre(self._music_genre)

    @music_genre.setter
    def music_genre(self, value: MusicGenre | str) -> None:
        music_genre = value if isinstance(value, MusicGenre) else MusicGenre(value)
        self._music_genre = music_genre.value

    def publish(self) -> bool:
        return

    def cancel(self) -> bool:
        return

    def updateInfo(self, event_title: EventTitle | str, description: Text200 | str, start_time: object, end_time: object) -> bool:
        return

    def isFull(self) -> bool:
        return
