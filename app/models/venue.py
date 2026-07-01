from app.extensions import db
from app.domain.value_objects import Address, Capacity, City, Room, VenueName
from sqlalchemy.ext.hybrid import hybrid_property


class Venue(db.Model):
    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, primary_key=True)
    _venue_name = db.Column("venue_name", db.String(120), nullable=False)
    _address = db.Column("address", db.String(255), nullable=False)
    _city = db.Column("city", db.String(80), nullable=False)
    _room = db.Column("room", db.String(80), nullable=False)
    _capacity = db.Column("capacity", db.Integer, nullable=False)

    events = db.relationship("MusicEvent", back_populates="venue")

    @hybrid_property
    def venue_name(self) -> VenueName:
        return VenueName(self._venue_name)

    @venue_name.expression
    def venue_name(cls):
        return cls._venue_name

    @venue_name.setter
    def venue_name(self, value: VenueName) -> None:
        if not isinstance(value, VenueName):
            raise TypeError("venue_name must be a VenueName value object")
        self._venue_name = value.value

    @hybrid_property
    def address(self) -> Address:
        return Address(self._address)

    @address.expression
    def address(cls):
        return cls._address

    @address.setter
    def address(self, value: Address) -> None:
        if not isinstance(value, Address):
            raise TypeError("address must be an Address value object")
        self._address = value.value

    @hybrid_property
    def city(self) -> City:
        return City(self._city)

    @city.expression
    def city(cls):
        return cls._city

    @city.setter
    def city(self, value: City) -> None:
        if not isinstance(value, City):
            raise TypeError("city must be a City value object")
        self._city = value.value

    @hybrid_property
    def room(self) -> Room:
        return Room(self._room)

    @room.expression
    def room(cls):
        return cls._room

    @room.setter
    def room(self, value: Room) -> None:
        if not isinstance(value, Room):
            raise TypeError("room must be a Room value object")
        self._room = value.value

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

    def checkAvailability(self, start_time, end_time) -> bool:
        from app.models.music_event import MusicEvent
        conflicting_events = MusicEvent.query.filter(
            MusicEvent.venue_id == self.venue_id,
            MusicEvent.start_time < end_time,
            MusicEvent.end_time > start_time
        ).count()
        return conflicting_events == 0
