from flask import Blueprint


organizer_bp = Blueprint("organizer", __name__, url_prefix="/organizer")


@organizer_bp.route("/dashboard")
def dashboard() -> object:
    return


@organizer_bp.route("/events/<int:event_id>/participants")
def participants(event_id: int) -> object:
    return
