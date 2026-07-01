from app.domain.value_objects import Address, Capacity, City, Room, VenueName
from app.extensions import db


class Venue(db.Model):
    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, primary_key=True)
    _venue_name = db.Column("venue_name", db.String(120), nullable=False)
    _address = db.Column("address", db.String(255), nullable=False)
    _city = db.Column("city", db.String(80), nullable=False)
    _room = db.Column("room", db.String(80), nullable=False)
    _capacity = db.Column("capacity", db.Integer, nullable=False)

    events = db.relationship("MusicEvent", back_populates="venue")

    @property
    def venue_name(self) -> VenueName:
        return VenueName(self._venue_name)

    @venue_name.setter
    def venue_name(self, value: VenueName | str) -> None:
        venue_name = value if isinstance(value, VenueName) else VenueName(value)
        self._venue_name = venue_name.value

    @property
    def address(self) -> Address:
        return Address(self._address)

    @address.setter
    def address(self, value: Address | str) -> None:
        address = value if isinstance(value, Address) else Address(value)
        self._address = address.value

    @property
    def city(self) -> City:
        return City(self._city)

    @city.setter
    def city(self, value: City | str) -> None:
        city = value if isinstance(value, City) else City(value)
        self._city = city.value

    @property
    def room(self) -> Room:
        return Room(self._room)

    @room.setter
    def room(self, value: Room | str) -> None:
        room = value if isinstance(value, Room) else Room(value)
        self._room = room.value

    @property
    def capacity(self) -> Capacity:
        return Capacity(self._capacity)

    @capacity.setter
    def capacity(self, value: Capacity | int) -> None:
        capacity = value if isinstance(value, Capacity) else Capacity(value)
        self._capacity = capacity.value

    def checkAvailability(self, start_time: object, end_time: object) -> bool:
        return
