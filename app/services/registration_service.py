from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db
from app.models.payment import Payment
from app.models.registration import Registration
from app.models.ticket import Ticket


class RegistrationService:
    def registerEvent(
        self,
        participant_id: int,
        event_id: int,
        ticket_type: str = "standard",
        price: Decimal = Decimal("0.00"),
        payment_method: str = "card",
    ) -> int:
        registration = Registration(
            participant_id=participant_id,
            event_id=event_id,
        )
        db.session.add(registration)
        db.session.flush()

        ticket = Ticket(
            ticket_type=ticket_type,
            price=price,
            registration_id=registration.registration_id,
        )
        ticket.generateQRCode()
        db.session.add(ticket)

        now = datetime.now(timezone.utc)
        payment = Payment(
            amount=price,
            payment_method=payment_method,
            payment_time=now,
            registration_id=registration.registration_id,
        )
        payment.pay(price, payment_method)
        db.session.add(payment)

        registration.confirmRegistration()
        db.session.commit()
        return registration.registration_id

    def cancelRegistration(self, registration_id: int) -> bool:
        registration = db.session.get(Registration, registration_id)
        if registration is None:
            return False
        registration.cancelRegistration()
        if registration.ticket:
            registration.ticket.cancelTicket()
        return True

    def markCheckedIn(self, registration_id: int) -> bool:
        registration = db.session.get(Registration, registration_id)
        if registration is None:
            return False
        registration.markCheckedIn()
        return True

    def getRegistrationsByParticipant(self, participant_id: int) -> list[Registration]:
        return (
            Registration.query
            .filter_by(participant_id=participant_id)
            .order_by(Registration.registration_time.desc())
            .all()
        )
