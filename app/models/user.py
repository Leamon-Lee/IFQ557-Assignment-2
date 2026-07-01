from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)
    user_type = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type,
    }

    def get_id(self) -> str:
        return str(self.user_id)

    def login(self, email: str, password_hash: str) -> bool:
        return

    def logout(self) -> bool:
        return

    def signup(self, nickname: str, email: str, password_hash: str) -> bool:
        return

    def updateProfile(self, nickname: str, email: str) -> bool:
        return
