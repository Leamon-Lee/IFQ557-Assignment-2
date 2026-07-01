from decimal import Decimal

from app.domain.value_objects import Money, PaymentMethod
from app.extensions import db
from app.models.payment import Payment


class PaymentService:
    def pay(self, registration_id: int, amount: Decimal, payment_method: str) -> bool:
        payment = Payment.query.filter_by(registration_id=registration_id).first()
        if payment is None:
            return False
        return payment.pay(Money(amount), PaymentMethod(payment_method))

    def refund(self, payment_id: int) -> bool:
        payment = db.session.get(Payment, payment_id)
        if payment is None:
            return False
        return payment.refund(payment.amount)

    def verifyPayment(self, payment_id: int) -> bool:
        payment = db.session.get(Payment, payment_id)
        return payment is not None and payment.payment_status == "Paid"
