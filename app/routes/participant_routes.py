from flask import Blueprint, render_template


participant_bp = Blueprint("participant", __name__, url_prefix="/participant")


@participant_bp.route("/dashboard")
def dashboard() -> object:
    return render_template("participant/dashboard.html")


@participant_bp.route("/registrations")
def registrations() -> object:
    return render_template("participant/registrations.html")


@participant_bp.route("/events/<int:event_id>/register", methods=["POST"])
def register_event(event_id: int) -> object:
    return


@participant_bp.route("/tickets/<int:ticket_id>")
def ticket(ticket_id: int) -> object:
    return render_template("participant/ticket.html")
