from decimal import Decimal

from app.domain.value_objects import Money, PaymentMethod, PaymentStatus
from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    _amount = db.Column("amount", db.Numeric(10, 2), nullable=False)
    _payment_method = db.Column("payment_method", db.String(30), nullable=False)
    _payment_status = db.Column("payment_status", db.String(30), nullable=False)
    payment_time = db.Column(db.DateTime, nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="payment")

    @property
    def amount(self) -> Money:
        return Money(self._amount)

    @amount.setter
    def amount(self, value: Money | Decimal) -> None:
        amount = value if isinstance(value, Money) else Money(value)
        self._amount = amount.value

    @property
    def payment_method(self) -> PaymentMethod:
        return PaymentMethod(self._payment_method)

    @payment_method.setter
    def payment_method(self, value: PaymentMethod | str) -> None:
        payment_method = value if isinstance(value, PaymentMethod) else PaymentMethod(value)
        self._payment_method = payment_method.value

    @property
    def payment_status(self) -> PaymentStatus:
        return PaymentStatus(self._payment_status)

    @payment_status.setter
    def payment_status(self, value: PaymentStatus | str) -> None:
        payment_status = value if isinstance(value, PaymentStatus) else PaymentStatus(value)
        self._payment_status = payment_status.value

    def pay(self, amount: Money | Decimal, payment_method: PaymentMethod | str) -> bool:
        return

    def refund(self, amount: Money | Decimal) -> bool:
        return

    def verifyPayment(self, payment_id: int) -> bool:
        return
