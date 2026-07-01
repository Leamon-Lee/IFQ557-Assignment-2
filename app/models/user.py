from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.domain.value_objects import Email, Nickname, PasswordHash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    _nickname = db.Column("nickname", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password_hash = db.Column("password_hash", db.String(255), nullable=False)
    _user_type = db.Column("user_type", db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": _user_type,
    }

    @property
    def nickname(self) -> Nickname:
        return Nickname(self._nickname)

    @nickname.setter
    def nickname(self, value: Nickname) -> None:
        if not isinstance(value, Nickname):
            raise TypeError("nickname must be a Nickname value object")
        self._nickname = value.value

    @property
    def email(self) -> Email:
        return Email(self._email)

    @email.setter
    def email(self, value: Email) -> None:
        if not isinstance(value, Email):
            raise TypeError("email must be an Email value object")
        self._email = value.value

    @property
    def password_hash(self) -> PasswordHash:
        return PasswordHash(self._password_hash)

    @password_hash.setter
    def password_hash(self, value: PasswordHash) -> None:
        if not isinstance(value, PasswordHash):
            raise TypeError("password_hash must be a PasswordHash value object")
        self._password_hash = value.value

    def get_id(self) -> str:
        return str(self.user_id)

    def login(self, email: Email, password: str) -> bool:
        user = User.query.filter(User._email == email.value).first()
        if user and check_password_hash(user.password_hash.value, password):
            return True
        return False

    def logout(self) -> bool:
        return True

    def signup(self, nickname: Nickname, email: Email, password: str) -> bool:
        if User.query.filter(User._email == email.value).first():
            return False
        self.nickname = nickname
        self.email = email
        self.password_hash = PasswordHash(generate_password_hash(password))
        db.session.add(self)
        db.session.commit()
        return True

    def updateProfile(self, nickname: Nickname, email: Email) -> bool:
        try:
            self.nickname = nickname
            self.email = email
            db.session.commit()
            return True
        except (TypeError, ValueError):
            db.session.rollback()
            return False
