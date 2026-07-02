from flask import Blueprint
from flask_login import current_user, login_required

from app.domain.value_objects import EventStatus
from app.extensions import db
from app.models.music_event import MusicEvent
from app.models.registration import Registration
from app.models.user import User
from app.routes.api_common import error, event_summary, require_role, success


api_admin_bp = Blueprint("api_admin", __name__, url_prefix="/api/admin")


@api_admin_bp.get("/dashboard/stats")
@login_required
def dashboard_stats():
    role_error = require_role("admin")
    if role_error:
        return role_error
    return success(data={
        "total_events": MusicEvent.query.count(),
        "total_users": User.query.count(),
        "total_registrations": Registration.query.count(),
        "open_events": MusicEvent.query.filter_by(_event_status="Open").count(),
    })


@api_admin_bp.get("/events")
@login_required
def list_events_for_review():
    role_error = require_role("admin")
    if role_error:
        return role_error
    events = MusicEvent.query.order_by(MusicEvent.start_time.desc()).all()
    return success(data={"events": [event_summary(e) for e in events]})


@api_admin_bp.post("/events/<int:event_id>/approve")
@login_required
def approve_event(event_id: int):
    role_error = require_role("admin")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    event.event_status = EventStatus("Open")
    db.session.commit()
    return success("Event approved.", {"event_status": str(event.event_status)})


@api_admin_bp.post("/events/<int:event_id>/reject")
@login_required
def reject_event(event_id: int):
    role_error = require_role("admin")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    event.event_status = EventStatus("Cancelled")
    db.session.commit()
    return success("Event rejected.", {"event_status": str(event.event_status)})