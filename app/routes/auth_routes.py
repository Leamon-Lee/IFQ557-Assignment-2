from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms.auth_forms import LoginForm, SignupForm
from app.domain.value_objects import Address, ContactNumber, Email, Name, Nickname
from app.models.participant import Participant
from app.models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("events.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = Email(form.email.data)
        user = User.query.filter(User._email == email.value).first()
        if user and user.login(email, form.password.data):
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("events.index"))
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("events.index"))

    form = SignupForm()
    if form.validate_on_submit():
        nickname = Nickname(form.nickname.data)
        email = Email(form.email.data)
        new_user = Participant(
            nickname=nickname,
            email=email,
            first_name=Name(form.first_name.data),
            second_name=Name(form.second_name.data),
            contact_number=ContactNumber(form.contact_number.data),
            street_address=Address(form.street_address.data),
        )
        if new_user.signup(nickname, email, form.password.data):
            flash("Account created! Please log in.", "success")
            return redirect(url_for("auth.login"))
        flash("This email is already registered.", "danger")

    return render_template("auth/signup.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("events.index"))
