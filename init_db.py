from app import create_app
from app.extensions import db
from app.models import Admin, Artist, MusicEvent, Organizer, Participant, Payment, Registration, Ticket, User, Venue


app = create_app()


with app.app_context():
    db.create_all()
