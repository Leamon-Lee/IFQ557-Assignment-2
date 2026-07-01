from flask import Blueprint


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> object:
    return


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup() -> object:
    return


@auth_bp.route("/logout")
def logout() -> object:
    return
