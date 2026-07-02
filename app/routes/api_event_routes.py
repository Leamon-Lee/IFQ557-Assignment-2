from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, request
from flask_login import current_user, login_required

from app.domain.value_objects import AgeRestriction, Capacity, DateTime, EventStatus, EventTitle, MusicGenre, Text200
from app.extensions import db
from app.models.music_event import MusicEvent
from app.routes.api_common import error, event_summary, iso, payload, require_role, success
from app.services.comment_service import CommentService
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService


api_event_bp = Blueprint("api_event", __name__, url_prefix="/api/events")


@api_event_bp.get("")
def list_events():
    service = EventService()
    events = service.listEvents(
        genre=request.args.get("genre") or None,
        search=request.args.get("search") or None,
        date_filter=request.args.get("date") or None,
    )
    return success(data={"events": [event_summary(event) for event in events]})


@api_event_bp.get("/<int:event_id>")
def event_detail(event_id: int):
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)

    data = event_summary(event)
    data.update({
        "venue": {
            "venue_id": event.venue.venue_id,
            "venue_name": str(event.venue.venue_name),
            "address": str(event.venue.address),
            "city": str(event.venue.city),
            "room": str(event.venue.room),
        } if event.venue else None,
        "artists": [
            {
                "artist_id": artist.artist_id,
                "first_name": str(artist.first_name),
                "second_name": str(artist.second_name),
                "music_genre": str(artist.music_genre),
            }
            for artist in event.artists
        ],
        "comments": [
            {
                "comment_id": comment.comment_id,
                "content": str(comment.content),
                "created_at": iso(comment.created_at),
            }
            for comment in event.comments
        ],
        "announcements": [
            {
                "announcement_id": announcement.announcement_id,
                "content": str(announcement.content),
                "created_at": iso(announcement.created_at),
            }
            for announcement in event.announcements
        ],
    })
    return success(data=data)


@api_event_bp.post("")
@login_required
def create_event():
    role_error = require_role("organizer")
    if role_error:
        return role_error
    data = payload()
    try:
        event = MusicEvent(
            event_title=EventTitle(data.get("event_title", "")),
            description=Text200(data.get("description", "")),
            music_genre=MusicGenre(data.get("music_genre", "")),
            venue_id=int(data.get("venue_id")),
            start_time=DateTime(datetime.fromisoformat(data.get("start_time", ""))),
            end_time=DateTime(datetime.fromisoformat(data.get("end_time", ""))),
            capacity=Capacity(int(data.get("capacity", 0))),
            age_restriction=AgeRestriction(int(data.get("age_restriction", 0))),
            event_status=EventStatus("Open"),
            organizer_id=current_user.organizer_id,
        )
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)

    db.session.add(event)
    db.session.commit()
    return success("Event created.", event_summary(event), 201)


@api_event_bp.put("/<int:event_id>")
@login_required
def update_event(event_id: int):
    role_error = require_role("organizer")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    if event.organizer_id != current_user.organizer_id:
        return error("You can only update your own events.", 403)

    data = payload()
    try:
        if "event_title" in data:
            event.event_title = EventTitle(data["event_title"])
        if "description" in data:
            event.description = Text200(data["description"])
        if "music_genre" in data:
            event.music_genre = MusicGenre(data["music_genre"])
        if "event_status" in data:
            event.event_status = EventStatus(data["event_status"])
        if "venue_id" in data:
            event.venue_id = int(data["venue_id"])
        if "start_time" in data:
            event.start_time = DateTime(datetime.fromisoformat(data["start_time"]))
        if "end_time" in data:
            event.end_time = DateTime(datetime.fromisoformat(data["end_time"]))
        if "capacity" in data:
            event.capacity = Capacity(int(data["capacity"]))
        if "age_restriction" in data:
            event.age_restriction = AgeRestriction(int(data["age_restriction"]))
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)

    db.session.commit()
    return success("Event updated.", event_summary(event))


@api_event_bp.post("/<int:event_id>/cancel")
@login_required
def cancel_event(event_id: int):
    role_error = require_role("organizer")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    if event.organizer_id != current_user.organizer_id:
        return error("You can only cancel your own events.", 403)
    event.cancel()
    return success("Event cancelled.", {"event_status": str(event.event_status)})


@api_event_bp.post("/<int:event_id>/book")
@login_required
def book_event(event_id: int):
    role_error = require_role("participant")
    if role_error:
        return role_error
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        return error("Event not found.", 404)
    if event.event_status != "Open":
        return error("This event is not open for booking.", 400)

    data = payload()
    try:
        quantity = max(1, int(data.get("quantity", 1)))
        price = Decimal(str(data.get("price", "0.00")))
    except (ValueError, InvalidOperation) as exc:
        return error(str(exc), 400)

    service = EventService()
    remaining = service.getRemainingTickets(event_id)
    if quantity > remaining:
        return error("Not enough tickets remaining.", 400)

    reg_service = RegistrationService()
    order_ids = []
    for _ in range(quantity):
        registration_id = reg_service.registerEvent(
            participant_id=current_user.participant_id,
            event_id=event_id,
            ticket_type=data.get("ticket_type", "standard"),
            price=price,
            payment_method=data.get("payment_method", "card"),
        )
        order_ids.append(f"SW-{event.start_time.year}-{registration_id:04d}")
    return success("Booking confirmed.", {"order_ids": order_ids}, 201)


@api_event_bp.post("/<int:event_id>/comments")
@login_required
def post_comment(event_id: int):
    if db.session.get(MusicEvent, event_id) is None:
        return error("Event not found.", 404)
    data = payload()
    try:
        comment = CommentService().addComment(current_user.user_id, event_id, data.get("content", "").strip())
    except (TypeError, ValueError) as exc:
        return error(str(exc), 400)
    return success("Comment posted.", {
        "comment_id": comment.comment_id,
        "content": str(comment.content),
        "created_at": iso(comment.created_at),
    }, 201)
