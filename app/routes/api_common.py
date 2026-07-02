from flask import jsonify, request
from flask_login import current_user

from app.models.music_event import MusicEvent
from app.models.organizer import Organizer
from app.models.participant import Participant
from app.models.registration import Registration
from app.models.user import User
from app.services.event_service import EventService


def payload() -> dict:
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()


def success(message: str = "Operation completed.", data: dict | list | None = None, status: int = 200):
    return jsonify({"success": True, "message": message, "data": data or {}}), status


def error(message: str, status: int = 400, errors: dict | None = None):
    return jsonify({"success": False, "message": message, "errors": errors or {}}), status


def role_for(user: User) -> str:
    if isinstance(user, Organizer):
        return "organizer"
    if isinstance(user, Participant):
        return "participant"
    return "admin" if user.__class__.__name__ == "Admin" else "user"


def redirect_for(role: str) -> str:
    if role == "organizer":
        return "/organizer/dashboard"
    if role == "admin":
        return "/admin/dashboard"
    return "/participant/registrations"


def iso(value) -> str | None:
    raw = getattr(value, "value", value)
    return raw.isoformat() if raw else None


def event_summary(event: MusicEvent) -> dict:
    service = EventService()
    return {
        "event_id": event.event_id,
        "event_title": str(event.event_title),
        "description": str(event.description),
        "music_genre": str(event.music_genre),
        "venue_name": str(event.venue.venue_name) if event.venue else "TBA",
        "start_time": iso(event.start_time),
        "end_time": iso(event.end_time),
        "capacity": int(event.capacity),
        "age_restriction": int(event.age_restriction),
        "event_status": str(event.event_status),
        "remaining_tickets": service.getRemainingTickets(event.event_id),
    }


def registration_data(registration: Registration) -> dict:
    ticket = registration.ticket
    payment = registration.payment
    return {
        "registration_id": registration.registration_id,
        "registration_time": iso(registration.registration_time),
        "registration_status": str(registration.registration_status),
        "check_in_status": str(registration.check_in_status),
        "event": event_summary(registration.music_event) if registration.music_event else None,
        "ticket": {
            "ticket_id": ticket.ticket_id,
            "ticket_type": str(ticket.ticket_type),
            "ticket_status": str(ticket.ticket_status),
            "price": str(ticket.price),
        } if ticket else None,
        "payment": {
            "payment_id": payment.payment_id,
            "payment_status": str(payment.payment_status),
            "amount": str(payment.amount),
        } if payment else None,
    }


def require_role(role: str):
    if not current_user.is_authenticated:
        return error("Authentication required.", 401)
    if role_for(current_user) != role:
        return error(f"{role.title()} account required.", 403)
    return None
