from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.announcement import Announcement
from app.models.music_event import MusicEvent
from app.models.organizer import Organizer
from app.models.registration import Registration
from app.services.event_service import EventService

organizer_bp = Blueprint("organizer", __name__, url_prefix="/organizer")


def _require_organizer():
    org = Organizer.query.filter_by(organizer_id=current_user.user_id).first()
    if org is None:
        flash("You need an organizer account to access this page.", "danger")
        return None
    return org


@organizer_bp.route("/dashboard")
@login_required
def dashboard():
    org = _require_organizer()
    if org is None:
        return redirect(url_for("events.index"))

    events = MusicEvent.query.filter_by(organizer_id=org.organizer_id).order_by(MusicEvent.start_time.desc()).all()
    service = EventService()

    event_data = []
    for e in events:
        confirmed = service.getConfirmedCount(e.event_id)
        event_data.append({
            "event": e,
            "confirmed": confirmed,
            "remaining": service.getRemainingTickets(e.event_id),
            "venue_name": e.venue.venue_name if e.venue else "TBA",
        })

    return render_template(
        "organizer/dashboard.html",
        organizer=org,
        events=event_data,
    )


@organizer_bp.route("/events/<int:event_id>/participants", methods=["GET", "POST"])
@login_required
def participants(event_id: int):
    org = _require_organizer()
    if org is None:
        return redirect(url_for("events.index"))

    event = db.session.get(MusicEvent, event_id)
    if event is None:
        abort(404)
    if event.organizer_id != org.organizer_id:
        flash("You can only view participants for your own events.", "danger")
        return redirect(url_for("organizer.dashboard"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            announcement = Announcement(content=content, event_id=event_id)
            db.session.add(announcement)
            db.session.commit()
            flash("Announcement posted.", "success")
        return redirect(url_for("organizer.participants", event_id=event_id))

    registrations = (
        Registration.query
        .filter_by(event_id=event_id)
        .order_by(Registration.registration_time.desc())
        .all()
    )

    announcements = (
        Announcement.query
        .filter_by(event_id=event_id)
        .order_by(Announcement.created_at.desc())
        .all()
    )

    return render_template(
        "organizer/participants.html",
        event=event,
        registrations=registrations,
        announcements=announcements,
    )
