from app.extensions import db
from app.domain.value_objects import DateTime, Money, PaymentMethod, PaymentStatus
from sqlalchemy.ext.hybrid import hybrid_property


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    _amount = db.Column("amount", db.Numeric(10, 2), nullable=False)
    _payment_method = db.Column("payment_method", db.String(30), nullable=False)
    _payment_status = db.Column("payment_status", db.String(30), nullable=False, default="Pending")
    _payment_time = db.Column("payment_time", db.DateTime, nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="payment")

    @hybrid_property
    def amount(self) -> Money:
        return Money(self._amount)

    @amount.expression
    def amount(cls):
        return cls._amount

    @amount.setter
    def amount(self, value: Money) -> None:
        if not isinstance(value, Money):
            raise TypeError("amount must be a Money value object")
        self._amount = value.value

    @hybrid_property
    def payment_method(self) -> PaymentMethod:
        return PaymentMethod(self._payment_method)

    @payment_method.expression
    def payment_method(cls):
        return cls._payment_method

    @payment_method.setter
    def payment_method(self, value: PaymentMethod) -> None:
        if not isinstance(value, PaymentMethod):
            raise TypeError("payment_method must be a PaymentMethod value object")
        self._payment_method = value.value

    @hybrid_property
    def payment_status(self) -> PaymentStatus:
        return PaymentStatus(self._payment_status or "Pending")

    @payment_status.expression
    def payment_status(cls):
        return cls._payment_status

    @payment_status.setter
    def payment_status(self, value: PaymentStatus) -> None:
        if not isinstance(value, PaymentStatus):
            raise TypeError("payment_status must be a PaymentStatus value object")
        self._payment_status = value.value

    @hybrid_property
    def payment_time(self) -> DateTime:
        return DateTime(self._payment_time)

    @payment_time.expression
    def payment_time(cls):
        return cls._payment_time

    @payment_time.setter
    def payment_time(self, value: DateTime) -> None:
        if not isinstance(value, DateTime):
            raise TypeError("payment_time must be a DateTime value object")
        self._payment_time = value.value

    def pay(self, amount: Money, payment_method: PaymentMethod) -> bool:
        if not isinstance(amount, Money):
            raise TypeError("amount must be a Money value object")
        if not isinstance(payment_method, PaymentMethod):
            raise TypeError("payment_method must be a PaymentMethod value object")
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = PaymentStatus("Paid")
        db.session.commit()
        return True

    def refund(self, amount: Money) -> bool:
        if not isinstance(amount, Money):
            raise TypeError("amount must be a Money value object")
        self.payment_status = PaymentStatus("Refunded")
        db.session.commit()
        return True

    def verifyPayment(self, payment_id: int) -> bool:
        payment = Payment.query.get(payment_id)
        return payment is not None and payment.payment_status == "Paid"
