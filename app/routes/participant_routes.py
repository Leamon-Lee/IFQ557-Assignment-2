from decimal import Decimal

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFError

from app.extensions import db
from app.models.music_event import MusicEvent
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService

participant_bp = Blueprint("participant", __name__, url_prefix="/participant")


@participant_bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash("Your session expired. Please try again.", "danger")
    return redirect(url_for("events.index"))


@participant_bp.route("/dashboard")
@login_required
def dashboard():
    reg_service = RegistrationService()
    registrations = reg_service.getRegistrationsByParticipant(current_user.user_id)
    confirmed = [r for r in registrations if r.registration_status == "Confirmed"]
    total_tickets = len(confirmed)

    return render_template(
        "participant/dashboard.html",
        registrations=confirmed,
        total_tickets=total_tickets,
    )


@participant_bp.route("/registrations")
@login_required
def registrations():
    reg_service = RegistrationService()
    regs = reg_service.getRegistrationsByParticipant(current_user.user_id)

    return render_template("participant/registrations.html", registrations=regs)


@participant_bp.route("/events/<int:event_id>/register", methods=["POST"])
@login_required
def register_event(event_id: int):
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        abort(404)

    if event.event_status != "Open":
        flash("This event is no longer open for bookings.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    service = EventService()
    remaining = service.getRemainingTickets(event_id)
    if remaining <= 0:
        flash("Sorry, this event is fully booked.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    try:
        quantity = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1
    if quantity > remaining:
        quantity = remaining

    ticket_type = request.form.get("ticket_type", "standard")
    try:
        price = Decimal(request.form.get("price", "0.00"))
    except Exception:
        price = Decimal("0.00")
    payment_method = request.form.get("payment_method", "card")

    reg_service = RegistrationService()
    order_ids = []
    for _ in range(quantity):
        rid = reg_service.registerEvent(
            participant_id=current_user.user_id,
            event_id=event_id,
            ticket_type=ticket_type,
            price=price,
            payment_method=payment_method,
        )
        order_ids.append(f"SW-{event.start_time.year}-{rid:04d}")

    if len(order_ids) == 1:
        flash(f"Booking confirmed! Your order ID is {order_ids[0]}.", "success")
    else:
        flash(f"Booked {len(order_ids)} tickets. Order IDs: {', '.join(order_ids)}.", "success")

    return redirect(url_for("participant.registrations"))


@participant_bp.route("/tickets/<int:ticket_id>")
@login_required
def ticket(ticket_id: int):
    return render_template("participant/ticket.html")
