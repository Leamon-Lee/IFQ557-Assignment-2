from app.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    qr_code = db.Column(db.String(255), nullable=False, unique=True)
    ticket_status = db.Column(db.String(30), nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.registration_id"), nullable=False, unique=True)

    registration = db.relationship("Registration", back_populates="ticket")

    def generateQRCode(self) -> str:
        return

    def validateTicket(self, qr_code: str) -> bool:
        return

    def cancelTicket(self) -> bool:
        return
