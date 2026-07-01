from decimal import Decimal

from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    payment_status = db.Column(db.String(30), nullable=False)
    payment_time = db.Column(db.DateTime, nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="payment")

    def pay(self, amount: Decimal, payment_method: str) -> bool:
        return

    def refund(self, amount: Decimal) -> bool:
        return

    def verifyPayment(self, payment_id: int) -> bool:
        return
