from app.extensions import db
from app.domain.value_objects import AgeRestriction, Capacity, DateTime, EventStatus, EventTitle, MusicGenre, Text200
from sqlalchemy.ext.hybrid import hybrid_property


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
    _start_time = db.Column("start_time", db.DateTime, nullable=False)
    _end_time = db.Column("end_time", db.DateTime, nullable=False)
    _capacity = db.Column("capacity", db.Integer, nullable=False)
    _age_restriction = db.Column("age_restriction", db.Integer, nullable=False)
    _event_status = db.Column("event_status", db.String(30), nullable=False, default="Open")
    _music_genre = db.Column("music_genre", db.String(80), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizers.organizer_id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.venue_id"), nullable=False)

    organizer = db.relationship("Organizer", back_populates="events")
    venue = db.relationship("Venue", back_populates="events")
    artists = db.relationship("Artist", secondary=event_artist, back_populates="events")
    registrations = db.relationship("Registration", back_populates="music_event")
    comments = db.relationship("Comment", back_populates="music_event")
    announcements = db.relationship("Announcement", back_populates="music_event")

    @hybrid_property
    def event_title(self) -> EventTitle:
        return EventTitle(self._event_title)

    @event_title.expression
    def event_title(cls):
        return cls._event_title

    @event_title.setter
    def event_title(self, value: EventTitle) -> None:
        if not isinstance(value, EventTitle):
            raise TypeError("event_title must be an EventTitle value object")
        self._event_title = value.value

    @hybrid_property
    def description(self) -> Text200:
        return Text200(self._description)

    @description.expression
    def description(cls):
        return cls._description

    @description.setter
    def description(self, value: Text200) -> None:
        if not isinstance(value, Text200):
            raise TypeError("description must be a Text200 value object")
        self._description = value.value

    @hybrid_property
    def start_time(self) -> DateTime:
        return DateTime(self._start_time)

    @start_time.expression
    def start_time(cls):
        return cls._start_time

    @start_time.setter
    def start_time(self, value: DateTime) -> None:
        if not isinstance(value, DateTime):
            raise TypeError("start_time must be a DateTime value object")
        self._start_time = value.value

    @hybrid_property
    def end_time(self) -> DateTime:
        return DateTime(self._end_time)

    @end_time.expression
    def end_time(cls):
        return cls._end_time

    @end_time.setter
    def end_time(self, value: DateTime) -> None:
        if not isinstance(value, DateTime):
            raise TypeError("end_time must be a DateTime value object")
        self._end_time = value.value

    @hybrid_property
    def capacity(self) -> Capacity:
        return Capacity(self._capacity)

    @capacity.expression
    def capacity(cls):
        return cls._capacity

    @capacity.setter
    def capacity(self, value: Capacity) -> None:
        if not isinstance(value, Capacity):
            raise TypeError("capacity must be a Capacity value object")
        self._capacity = value.value

    @hybrid_property
    def age_restriction(self) -> AgeRestriction:
        return AgeRestriction(self._age_restriction)

    @age_restriction.expression
    def age_restriction(cls):
        return cls._age_restriction

    @age_restriction.setter
    def age_restriction(self, value: AgeRestriction) -> None:
        if not isinstance(value, AgeRestriction):
            raise TypeError("age_restriction must be an AgeRestriction value object")
        self._age_restriction = value.value

    @hybrid_property
    def event_status(self) -> EventStatus:
        return EventStatus(self._event_status or "Open")

    @event_status.expression
    def event_status(cls):
        return cls._event_status

    @event_status.setter
    def event_status(self, value: EventStatus) -> None:
        if not isinstance(value, EventStatus):
            raise TypeError("event_status must be an EventStatus value object")
        self._event_status = value.value

    @hybrid_property
    def music_genre(self) -> MusicGenre:
        return MusicGenre(self._music_genre)

    @music_genre.expression
    def music_genre(cls):
        return cls._music_genre

    @music_genre.setter
    def music_genre(self, value: MusicGenre) -> None:
        if not isinstance(value, MusicGenre):
            raise TypeError("music_genre must be a MusicGenre value object")
        self._music_genre = value.value

    def publish(self) -> bool:
        self.event_status = EventStatus("Open")
        db.session.commit()
        return True

    def cancel(self) -> bool:
        self.event_status = EventStatus("Cancelled")
        db.session.commit()
        return True

    def updateInfo(self, event_title: EventTitle, description: Text200, start_time: DateTime, end_time: DateTime) -> bool:
        self.event_title = event_title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        db.session.commit()
        return True

    def isFull(self) -> bool:
        return len(self.registrations) >= int(self.capacity)
