from flask import Blueprint
from flask_login import current_user, login_required

from app.domain.value_objects import CheckInStatus, Text500, TicketStatus
from app.extensions import db
from app.models.announcement import Announcement
from app.models.music_event import MusicEvent
from app.models.registration import Registration
from app.routes.api_common import error, iso, payload, registration_data, require_role, success


api_organizer_bp = Blueprint("api_organizer", __name__, url_prefix="/api/organizer")


@api_organizer_bp.get("/events/<int:event_id>/participants")
@login_required
def event_participants(event_id: int):
    role_error = require_role("organizer")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    if event.organizer_id != current_user.organizer_id:
        return error("You can only view your own events.", 403)
    registrations = Registration.query.filter_by(event_id=event_id).order_by(Registration.registration_time.desc()).all()
    return success(data={"participants": [registration_data(registration) for registration in registrations]})


@api_organizer_bp.post("/registrations/<int:registration_id>/check-in")
@login_required
def check_in_registration(registration_id: int):
    role_error = require_role("organizer")
    if role_error:
        return role_error
    registration = db.session.get(Registration, registration_id)
    if registration is None:
        return error("Registration not found.", 404)
    if registration.music_event.organizer_id != current_user.organizer_id:
        return error("You can only check in participants for your own events.", 403)

    registration.check_in_status = CheckInStatus("CheckedIn")
    if registration.ticket:
        registration.ticket.ticket_status = TicketStatus("Used")
    db.session.commit()
    return success("Participant checked in.", {
        "check_in_status": str(registration.check_in_status),
        "ticket_status": str(registration.ticket.ticket_status) if registration.ticket else None,
    })


@api_organizer_bp.post("/events/<int:event_id>/announcements")
@login_required
def post_announcement(event_id: int):
    role_error = require_role("organizer")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    if event.organizer_id != current_user.organizer_id:
        return error("You can only announce on your own events.", 403)
    data = payload()
    try:
        announcement = Announcement(content=Text500(data.get("content", "").strip()), event_id=event_id)
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)
    db.session.add(announcement)
    db.session.commit()
    return success("Announcement posted.", {
        "announcement_id": announcement.announcement_id,
        "content": str(announcement.content),
        "created_at": iso(announcement.created_at),
    }, 201)
