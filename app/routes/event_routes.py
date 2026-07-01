from flask import Blueprint


event_bp = Blueprint("events", __name__)


@event_bp.route("/")
def index() -> object:
    return


@event_bp.route("/events")
def list_events() -> object:
    return


@event_bp.route("/events/<int:event_id>")
def event_detail(event_id: int) -> object:
    return


@event_bp.route("/events/create", methods=["GET", "POST"])
def create_event() -> object:
    return


@event_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id: int) -> object:
    return
