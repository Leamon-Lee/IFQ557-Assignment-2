from app.extensions import db
from app.domain.value_objects import Capacity, EventStatus, EventTitle, Name, OrganizationName, Text100
from .user import User


class Organizer(User):
    __tablename__ = "organizers"

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    _organization_name = db.Column("organization_name", db.String(120), nullable=False)
    _first_name = db.Column("first_name", db.String(30), nullable=False)
    _second_name = db.Column("second_name", db.String(30), nullable=False)
    _bio = db.Column("bio", db.String(100))

    events = db.relationship("MusicEvent", back_populates="organizer")

    __mapper_args__ = {
        "polymorphic_identity": "organizer",
    }

    @property
    def organization_name(self) -> OrganizationName:
        return OrganizationName(self._organization_name)

    @organization_name.setter
    def organization_name(self, value: OrganizationName | str) -> None:
        organization_name = value if isinstance(value, OrganizationName) else OrganizationName(value)
        self._organization_name = organization_name.value

    @property
    def first_name(self) -> Name:
        return Name(self._first_name)

    @first_name.setter
    def first_name(self, value: Name | str) -> None:
        name = value if isinstance(value, Name) else Name(value)
        self._first_name = name.value

    @property
    def second_name(self) -> Name:
        return Name(self._second_name)

    @second_name.setter
    def second_name(self, value: Name | str) -> None:
        name = value if isinstance(value, Name) else Name(value)
        self._second_name = name.value

    @property
    def bio(self) -> Text100:
        return Text100(self._bio or "")

    @bio.setter
    def bio(self, value: Text100 | str) -> None:
        bio = value if isinstance(value, Text100) else Text100(value)
        self._bio = bio.value

    def createEvent(self, title: EventTitle | str, description: str, start_time: object, end_time: object, capacity: Capacity | int) -> int:
        from app.models.music_event import MusicEvent
        event_title = title if isinstance(title, EventTitle) else EventTitle(title)
        event_capacity = capacity if isinstance(capacity, Capacity) else Capacity(capacity)
        new_event = MusicEvent(
            event_title=event_title.value,
            description=description,
            start_time=start_time,
            end_time=end_time,
            capacity=event_capacity.value,
            organizer_id=self.organizer_id
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event.event_id

    def updateEvent(self, event_id: int, **kwargs) -> bool:
        from app.models.music_event import MusicEvent
        event = MusicEvent.query.filter_by(event_id=event_id, organizer_id=self.organizer_id).first()
        if event:
            for key, value in kwargs.items():
                setattr(event, key, value)
            db.session.commit()
            return True
        return False

    def cancelEvent(self, event_id: int) -> bool:
        from app.models.music_event import MusicEvent
        event = MusicEvent.query.filter_by(event_id=event_id, organizer_id=self.organizer_id).first()
        if event:
            event.event_status = EventStatus("cancelled").value
            db.session.commit()
            return True
        return False

    def viewParticipants(self, event_id: int) -> list:
        from app.models.registration import Registration
        return Registration.query.filter_by(event_id=event_id).all()

    def sendAnnouncement(self, event_id: int, message: str) -> bool:
        return True
