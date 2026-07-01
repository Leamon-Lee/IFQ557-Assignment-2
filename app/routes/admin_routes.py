from flask import Blueprint, abort, flash, redirect, render_template, url_for

from app.domain.value_objects import EventStatus
from app.extensions import db
from app.models.admin import Admin
from app.models.music_event import MusicEvent
from app.models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
def dashboard():
    total_events = MusicEvent.query.count()
    total_users = User.query.count()
    open_events = MusicEvent.query.filter_by(event_status="Open").count()
    recent_events = MusicEvent.query.order_by(MusicEvent.start_time.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_events=total_events,
        total_users=total_users,
        open_events=open_events,
        recent_events=recent_events,
    )


@admin_bp.route("/review-events")
def review_events():
    events = MusicEvent.query.order_by(MusicEvent.start_time.desc()).all()
    return render_template("admin/review_events.html", events=events)


@admin_bp.route("/events/<int:event_id>/approve", methods=["POST"])
def approve_event(event_id: int):
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        abort(404)
    event.event_status = EventStatus("Open")
    db.session.commit()
    flash(f"Event '{event.event_title}' has been approved.", "success")
    return redirect(url_for("admin.review_events"))


@admin_bp.route("/events/<int:event_id>/reject", methods=["POST"])
def reject_event(event_id: int):
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        abort(404)
    event.event_status = EventStatus("Cancelled")
    db.session.commit()
    flash(f"Event '{event.event_title}' has been rejected.", "info")
    return redirect(url_for("admin.review_events"))
