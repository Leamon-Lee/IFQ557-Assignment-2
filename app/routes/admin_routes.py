from flask import Blueprint, render_template


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
def dashboard() -> object:
    return render_template("admin/dashboard.html")


@admin_bp.route("/review-events")
def review_events() -> object:
    return render_template("admin/review_events.html")


@admin_bp.route("/events/<int:event_id>/approve", methods=["POST"])
def approve_event(event_id: int) -> object:
    return


@admin_bp.route("/events/<int:event_id>/reject", methods=["POST"])
def reject_event(event_id: int) -> object:
    return
