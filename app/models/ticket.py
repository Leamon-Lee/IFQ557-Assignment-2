import uuid

from app.extensions import db
from app.domain.value_objects import Money, QRCode, TicketStatus, TicketType
from sqlalchemy.ext.hybrid import hybrid_property


class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True)
    _ticket_type = db.Column("ticket_type", db.String(30), nullable=False)
    _price = db.Column("price", db.Numeric(10, 2), nullable=False)
    _qr_code = db.Column("qr_code", db.String(255), nullable=False, unique=True)
    _ticket_status = db.Column("ticket_status", db.String(30), nullable=False, default="Valid")
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="ticket")

    @hybrid_property
    def ticket_type(self) -> TicketType:
        return TicketType(self._ticket_type)

    @ticket_type.expression
    def ticket_type(cls):
        return cls._ticket_type

    @ticket_type.setter
    def ticket_type(self, value: TicketType) -> None:
        if not isinstance(value, TicketType):
            raise TypeError("ticket_type must be a TicketType value object")
        self._ticket_type = value.value

    @hybrid_property
    def price(self) -> Money:
        return Money(self._price)

    @price.expression
    def price(cls):
        return cls._price

    @price.setter
    def price(self, value: Money) -> None:
        if not isinstance(value, Money):
            raise TypeError("price must be a Money value object")
        self._price = value.value

    @hybrid_property
    def qr_code(self) -> QRCode:
        return QRCode(self._qr_code)

    @qr_code.expression
    def qr_code(cls):
        return cls._qr_code

    @qr_code.setter
    def qr_code(self, value: QRCode) -> None:
        if not isinstance(value, QRCode):
            raise TypeError("qr_code must be a QRCode value object")
        self._qr_code = value.value

    @hybrid_property
    def ticket_status(self) -> TicketStatus:
        return TicketStatus(self._ticket_status or "Valid")

    @ticket_status.expression
    def ticket_status(cls):
        return cls._ticket_status

    @ticket_status.setter
    def ticket_status(self, value: TicketStatus) -> None:
        if not isinstance(value, TicketStatus):
            raise TypeError("ticket_status must be a TicketStatus value object")
        self._ticket_status = value.value

    def generateQRCode(self) -> str:
        code = str(uuid.uuid4())
        self.qr_code = QRCode(code)
        db.session.commit()
        return code

    def validateTicket(self, qr_code: QRCode) -> bool:
        if not isinstance(qr_code, QRCode):
            raise TypeError("qr_code must be a QRCode value object")
        return self.qr_code == qr_code and self.ticket_status == "Valid"

    def cancelTicket(self) -> bool:
        self.ticket_status = TicketStatus("Cancelled")
        db.session.commit()
        return True
