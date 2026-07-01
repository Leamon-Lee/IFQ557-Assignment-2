from app.domain.value_objects import Email, Nickname, PasswordHash
from app.extensions import db


class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    _admin_name = db.Column("admin_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password_hash = db.Column("password_hash", db.String(255), nullable=False)

    @property
    def admin_name(self) -> Nickname:
        return Nickname(self._admin_name)

    @admin_name.setter
    def admin_name(self, value: Nickname | str) -> None:
        admin_name = value if isinstance(value, Nickname) else Nickname(value)
        self._admin_name = admin_name.value

    @property
    def email(self) -> Email:
        return Email(self._email)

    @email.setter
    def email(self, value: Email | str) -> None:
        email = value if isinstance(value, Email) else Email(value)
        self._email = email.value

    @property
    def password_hash(self) -> PasswordHash:
        return PasswordHash(self._password_hash)

    @password_hash.setter
    def password_hash(self, value: PasswordHash | str) -> None:
        password_hash = value if isinstance(value, PasswordHash) else PasswordHash(value)
        self._password_hash = password_hash.value

    def reviewEvent(self, event_id: int) -> bool:
        return

    def approveEvent(self, event_id: int) -> bool:
        return

    def rejectEvent(self, event_id: int) -> bool:
        return

    def manageUsers(self, user_id: int) -> bool:
        return

    def generateReport(self) -> str:
        return
