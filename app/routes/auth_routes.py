from flask import Blueprint, render_template


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> object:
    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup() -> object:
    return render_template("auth/signup.html")


@auth_bp.route("/logout")
def logout() -> object:
    return
