from app.extensions import db


class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def reviewEvent(self, event_id: int) -> bool:
        return

    def approveEvent(self, event_id: int) -> bool:
        return

    def rejectEvent(self, event_id: int) -> bool:
        return

    def manageUsers(self, user_id: int) -> bool:
        return

    def generateReport(self) -> str:
        return
