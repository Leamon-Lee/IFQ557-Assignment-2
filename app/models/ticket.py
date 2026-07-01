import uuid

from app.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    qr_code = db.Column(db.String(255), nullable=False, unique=True)
    ticket_status = db.Column(db.String(30), nullable=False, default="Valid")
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="ticket")

    def generateQRCode(self) -> str:
        code = str(uuid.uuid4())
        self.qr_code = code
        db.session.commit()
        return code

    def validateTicket(self, qr_code: str) -> bool:
        return self.qr_code == qr_code and self.ticket_status == "Valid"

    def cancelTicket(self) -> bool:
        self.ticket_status = "Cancelled"
        db.session.commit()
        return True
