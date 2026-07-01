from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms.auth_forms import LoginForm, SignupForm
from app.models.participant import Participant
from app.models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("events.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.login(form.email.data, form.password.data):
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
        new_user = Participant(
            nickname=form.nickname.data,
            email=form.email.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            contact_number=form.contact_number.data,
            street_address=form.street_address.data,
        )
        if new_user.signup(form.nickname.data, form.email.data, form.password.data):
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
