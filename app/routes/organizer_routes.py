from flask import Blueprint, render_template


organizer_bp = Blueprint("organizer", __name__, url_prefix="/organizer")


@organizer_bp.route("/dashboard")
def dashboard() -> object:
    return render_template("organizer/dashboard.html")


@organizer_bp.route("/events/<int:event_id>/participants")
def participants(event_id: int) -> object:
    return render_template("organizer/participants.html")
