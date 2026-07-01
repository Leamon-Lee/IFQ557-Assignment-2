from flask_login import login_user, logout_user

from app.domain.value_objects import Address, ContactNumber, Email, Name, Nickname, PasswordHash
from app.extensions import bcrypt, db
from app.models.participant import Participant
from app.models.user import User


class AuthService:
    def login(self, email: str, password: str):
        email_value = Email(email)
        user = User.query.filter(User._email == email_value.value).first()
        if user is None:
            return False, None, "No account found with this email."
        if not bcrypt.check_password_hash(user.password_hash.value, password):
            return False, None, "Incorrect password."
        login_user(user)
        return True, user, "Login successful."

    def signup(
        self,
        nickname: str,
        email: str,
        password: str,
        first_name: str,
        second_name: str,
        contact_number: str,
        street_address: str,
    ):
        nickname_value = Nickname(nickname)
        email_value = Email(email)
        first_name_value = Name(first_name)
        second_name_value = Name(second_name)
        contact_number_value = ContactNumber(contact_number)
        street_address_value = Address(street_address)

        existing = User.query.filter(User._email == email_value.value).first()
        if existing:
            return False, None, "This email is already registered."

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = Participant(
            nickname=nickname_value,
            email=email_value,
            password_hash=PasswordHash(password_hash),
            contact_number=contact_number_value,
            street_address=street_address_value,
            first_name=first_name_value,
            second_name=second_name_value,
        )
        db.session.add(new_user)
        db.session.commit()
        return True, new_user, "Registration successful."

    def logout(self):
        logout_user()
        return True
