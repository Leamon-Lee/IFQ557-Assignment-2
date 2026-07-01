from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.forms.auth_forms import LoginForm, SignupForm
from app.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # 如果用户已经登录，直接跳转首页
    if current_user.is_authenticated:
        return redirect(url_for("events.index"))

    form = LoginForm()
    if form.validate_on_submit():
        service = AuthService()
        success, user, message = service.login(
            email=form.email.data,
            password=form.password.data,
        )
        if success:
            flash(message, "success")
            return redirect(url_for("events.index"))
        flash(message, "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("events.index"))

    form = SignupForm()
    if form.validate_on_submit():
        service = AuthService()
        success, user, message = service.signup(
            nickname=form.nickname.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            contact_number=form.contact_number.data,
            street_address=form.street_address.data,
        )
        if success:
            flash("Account created! Please log in.", "success")
            return redirect(url_for("auth.login"))
        flash(message, "danger")
    return render_template("auth/signup.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    service = AuthService()
    service.logout()
    flash("You have been logged out.", "info")
    return redirect(url_for("events.index"))
