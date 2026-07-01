from werkzeug.security import generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from app.domain.value_objects import Email, EventStatus, Nickname, PasswordHash
from app.extensions import db


class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    _admin_name = db.Column("admin_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password_hash = db.Column("password_hash", db.String(255), nullable=False)

    @hybrid_property
    def admin_name(self) -> Nickname:
        return Nickname(self._admin_name)

    @admin_name.expression
    def admin_name(cls):
        return cls._admin_name

    @admin_name.setter
    def admin_name(self, value: Nickname) -> None:
        if not isinstance(value, Nickname):
            raise TypeError("admin_name must be a Nickname value object")
        self._admin_name = value.value

    @hybrid_property
    def email(self) -> Email:
        return Email(self._email)

    @email.expression
    def email(cls):
        return cls._email

    @email.setter
    def email(self, value: Email) -> None:
        if not isinstance(value, Email):
            raise TypeError("email must be an Email value object")
        self._email = value.value

    @hybrid_property
    def password_hash(self) -> PasswordHash:
        return PasswordHash(self._password_hash)

    @password_hash.expression
    def password_hash(cls):
        return cls._password_hash

    @password_hash.setter
    def password_hash(self, value: PasswordHash) -> None:
        if not isinstance(value, PasswordHash):
            raise TypeError("password_hash must be a PasswordHash value object")
        self._password_hash = value.value

    def set_password(self, password):
        self.password_hash = PasswordHash(generate_password_hash(password))

    def reviewEvent(self, event_id: int, status: EventStatus) -> bool:
        if not isinstance(status, EventStatus):
            raise TypeError("status must be an EventStatus value object")
        from app.models.music_event import MusicEvent
        event = MusicEvent.query.get(event_id)
        if event:
            event.event_status = status
            db.session.commit()
            return True
        return False

    def approveEvent(self, event_id: int) -> bool:
        return self.reviewEvent(event_id, EventStatus("Open"))

    def rejectEvent(self, event_id: int) -> bool:
        return self.reviewEvent(event_id, EventStatus("Cancelled"))

    def manageUsers(self, user_id: int) -> bool:
        return True

    def generateReport(self) -> str:
        from app.models.music_event import MusicEvent
        count = MusicEvent.query.count()
        return f"Total events in system: {count}"
