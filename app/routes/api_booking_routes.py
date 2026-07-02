from flask import Blueprint
from flask_login import current_user, login_required

from app.domain.value_objects import PaymentStatus
from app.extensions import db
from app.models.registration import Registration
from app.models.ticket import Ticket
from app.routes.api_common import error, registration_data, require_role, role_for, success
from app.services.registration_service import RegistrationService


api_booking_bp = Blueprint("api_booking", __name__, url_prefix="/api")


@api_booking_bp.get("/me/bookings")
@login_required
def my_bookings():
    role_error = require_role("participant")
    if role_error:
        return role_error
    registrations = RegistrationService().getRegistrationsByParticipant(current_user.participant_id)
    return success(data={"bookings": [registration_data(registration) for registration in registrations]})


@api_booking_bp.post("/bookings/<int:registration_id>/cancel")
@login_required
def cancel_booking(registration_id: int):
    role_error = require_role("participant")
    if role_error:
        return role_error
    registration = db.session.get(Registration, registration_id)
    if registration is None:
        return error("Booking not found.", 404)
    if registration.participant_id != current_user.participant_id:
        return error("You can only cancel your own bookings.", 403)

    registration.cancelRegistration()
    if registration.ticket:
        registration.ticket.cancelTicket()
    if registration.payment:
        registration.payment.payment_status = PaymentStatus("Refunded")
    db.session.commit()
    return success("Booking cancelled.", {
        "registration_status": str(registration.registration_status),
        "ticket_status": str(registration.ticket.ticket_status) if registration.ticket else None,
        "payment_status": str(registration.payment.payment_status) if registration.payment else None,
    })


@api_booking_bp.get("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id: int):
    ticket = db.session.get(Ticket, ticket_id)
    if ticket is None:
        return error("Ticket not found.", 404)
    if role_for(current_user) == "participant" and ticket.registration.participant_id != current_user.participant_id:
        return error("You can only view your own tickets.", 403)
    return success(data={
        "ticket_id": ticket.ticket_id,
        "ticket_type": str(ticket.ticket_type),
        "price": str(ticket.price),
        "qr_code": str(ticket.qr_code),
        "ticket_status": str(ticket.ticket_status),
        "registration_id": ticket.registration_id,
    })
