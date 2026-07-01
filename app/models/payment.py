from decimal import Decimal

from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    payment_status = db.Column(db.String(30), nullable=False, default="Pending")
    payment_time = db.Column(db.DateTime, nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="payment")

    def pay(self, amount: Decimal, payment_method: str) -> bool:
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = "Paid"
        db.session.commit()
        return True

    def refund(self, amount: Decimal) -> bool:
        self.payment_status = "Refunded"
        db.session.commit()
        return True

    def verifyPayment(self, payment_id: int) -> bool:
        payment = Payment.query.get(payment_id)
        return payment is not None and payment.payment_status == "Paid"
