from app.domain.value_objects import Money, QRCode, TicketStatus, TicketType
from app.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True)
    _ticket_type = db.Column("ticket_type", db.String(30), nullable=False)
    _price = db.Column("price", db.Numeric(10, 2), nullable=False)
    _qr_code = db.Column("qr_code", db.String(255), nullable=False, unique=True)
    _ticket_status = db.Column("ticket_status", db.String(30), nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="ticket")

    @property
    def ticket_type(self) -> TicketType:
        return TicketType(self._ticket_type)

    @ticket_type.setter
    def ticket_type(self, value: TicketType | str) -> None:
        ticket_type = value if isinstance(value, TicketType) else TicketType(value)
        self._ticket_type = ticket_type.value

    @property
    def price(self) -> Money:
        return Money(self._price)

    @price.setter
    def price(self, value: Money | object) -> None:
        price = value if isinstance(value, Money) else Money(value)
        self._price = price.value

    @property
    def qr_code(self) -> QRCode:
        return QRCode(self._qr_code)

    @qr_code.setter
    def qr_code(self, value: QRCode | str) -> None:
        qr_code = value if isinstance(value, QRCode) else QRCode(value)
        self._qr_code = qr_code.value

    @property
    def ticket_status(self) -> TicketStatus:
        return TicketStatus(self._ticket_status)

    @ticket_status.setter
    def ticket_status(self, value: TicketStatus | str) -> None:
        ticket_status = value if isinstance(value, TicketStatus) else TicketStatus(value)
        self._ticket_status = ticket_status.value

    def generateQRCode(self) -> str:
        return

    def validateTicket(self, qr_code: QRCode | str) -> bool:
        return

    def cancelTicket(self) -> bool:
        return
