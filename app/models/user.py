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

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": _user_type,
    }

    @property
    def nickname(self) -> Nickname:
        return Nickname(self._nickname)

    @nickname.setter
    def nickname(self, value: Nickname | str) -> None:
        nickname = value if isinstance(value, Nickname) else Nickname(value)
        self._nickname = nickname.value

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

    def get_id(self) -> str:
        return str(self.user_id)

    def login(self, email: Email | str, password: str) -> bool:
        valid_email = email if isinstance(email, Email) else Email(email)
        user = User.query.filter(User._email == valid_email.value).first()
        if user and check_password_hash(user.password_hash.value, password):
            return True
        return False

    def logout(self) -> bool:
        return True

    def signup(self, nickname: Nickname | str, email: Email | str, password: str) -> bool:
        valid_nickname = nickname if isinstance(nickname, Nickname) else Nickname(nickname)
        valid_email = email if isinstance(email, Email) else Email(email)
        if User.query.filter(User._email == valid_email.value).first():
            return False

        self.nickname = valid_nickname
        self.email = valid_email
        self.password_hash = generate_password_hash(password)

        db.session.add(self)
        db.session.commit()
        return True

    def updateProfile(self, nickname: Nickname | str, email: Email | str) -> bool:
        try:
            self.nickname = nickname
            self.email = email
            db.session.commit()
            return True
        except ValueError:
            db.session.rollback()
            return False
