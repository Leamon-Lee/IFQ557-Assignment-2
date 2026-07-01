from flask import Blueprint, render_template


event_bp = Blueprint("events", __name__)


@event_bp.route("/")
def index() -> object:
    return render_template("index.html")


@event_bp.route("/events")
def list_events() -> object:
    return render_template("events/list.html")


@event_bp.route("/events/<int:event_id>")
def event_detail(event_id: int) -> object:
    return render_template("events/detail.html")


@event_bp.route("/events/create", methods=["GET", "POST"])
def create_event() -> object:
    return render_template("events/create.html")


@event_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id: int) -> object:
    return render_template("events/edit.html")
