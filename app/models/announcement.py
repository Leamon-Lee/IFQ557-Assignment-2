from datetime import datetime, timezone

from app.extensions import db
from app.domain.value_objects import DateTime, Text500
from sqlalchemy.ext.hybrid import hybrid_property


class Announcement(db.Model):
    __tablename__ = "announcements"

    announcement_id = db.Column(db.Integer, primary_key=True)
    _content = db.Column("content", db.Text, nullable=False)
    _created_at = db.Column("created_at", db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    event_id = db.Column(db.Integer, db.ForeignKey("music_events.event_id"), nullable=False)

    music_event = db.relationship("MusicEvent", back_populates="announcements")

    @hybrid_property
    def content(self) -> Text500:
        return Text500(self._content)

    @content.expression
    def content(cls):
        return cls._content

    @content.setter
    def content(self, value: Text500) -> None:
        if not isinstance(value, Text500):
            raise TypeError("content must be a Text500 value object")
        self._content = value.value

    @hybrid_property
    def created_at(self) -> DateTime:
        return DateTime(self._created_at)

    @created_at.expression
    def created_at(cls):
        return cls._created_at

    @created_at.setter
    def created_at(self, value: DateTime) -> None:
        if not isinstance(value, DateTime):
            raise TypeError("created_at must be a DateTime value object")
        self._created_at = value.value
