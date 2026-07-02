from flask import Blueprint
from flask_login import login_user
from app.extensions import bcrypt

from app.domain.value_objects import (
    Address,
    ContactNumber,
    Email,
    Name,
    Nickname,
    OrganizationName,
    PasswordHash,
    Text100,
)
from app.extensions import db
from app.models.organizer import Organizer
from app.models.participant import Participant
from app.models.user import User
from app.routes.api_common import error, payload, redirect_for, role_for, success


api_auth_bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@api_auth_bp.post("/login")
def login():
    data = payload()
    try:
        email = Email(data.get("email", ""))
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)

    user = User.query.filter(User._email == email.value).first()
    if user is None or not bcrypt.check_password_hash(user.password_hash.value, data.get("password", "")):
        return error("Invalid email or password.", 401)

    role = role_for(user)
    requested_role = data.get("login_role")
    if requested_role and requested_role != role:
        return error("Selected role does not match this account.", 403)

    login_user(user)
    return success("Login successful.", {
        "user_id": user.user_id,
        "nickname": str(user.nickname),
        "role": role,
        "redirect_url": redirect_for(role),
    })


@api_auth_bp.post("/register")
def register():
    data = payload()
    account_type = data.get("account_type", "participant")
    if account_type not in {"participant", "organizer"}:
        return error("account_type must be participant or organizer.", 400)

    try:
        common = {
            "nickname": Nickname(data.get("nickname", "")),
            "email": Email(data.get("email", "")),
            "password_hash": PasswordHash(bcrypt.generate_password_hash(data.get("password", "")).decode("utf-8")),
            "contact_number": ContactNumber(data.get("contact_number", "")),
            "street_address": Address(data.get("street_address", "")),
            "first_name": Name(data.get("first_name", "")),
            "second_name": Name(data.get("second_name", "")),
        }
        if User.query.filter(User._email == common["email"].value).first():
            return error("This email is already registered.", 409)
        if account_type == "organizer":
            user = Organizer(
                **common,
                organization_name=OrganizationName(data.get("organization_name", "")),
                bio=Text100(data.get("bio", "")),
            )
        else:
            user = Participant(**common)
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)

    db.session.add(user)
    db.session.commit()
    return success("Account created.", {
        "user_id": user.user_id,
        "role": role_for(user),
        "redirect_url": "/auth/login",
    }, 201)
