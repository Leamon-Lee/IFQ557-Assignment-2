from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Organizer, Participant, MusicEvent, Venue, Artist, Registration, Ticket, Payment, Comment

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    now = datetime.now()

    # ---- 1. Users ----
    organizer = Organizer(
        nickname="music_live",
        email="organizer@soundwave.com",
        password_hash=generate_password_hash("123456"),
        contact_number="+86 138 0000 1111",
        street_address="10 Music Street",
        organization_name="SoundWave Productions",
        first_name="David",
        second_name="Lee",
        bio="Professional music event organizer.",
    )

    participant = Participant(
        nickname="alexchen",
        email="alex@soundwave.com",
        password_hash=generate_password_hash("123456"),
        contact_number="+86 138 0000 2222",
        street_address="88 Happy Road",
        first_name="Alex",
        second_name="Chen",
    )

    db.session.add_all([organizer, participant])
    db.session.flush()

    # ---- 2. Venues ----
    venues = [
        Venue(venue_name="Blue Hall", address="15 Riverside Ave", city="Shanghai", room="Hall A", capacity=100),
        Venue(venue_name="Main Lawn", address="22 University Blvd", city="Beijing", room="Outdoor Stage", capacity=500),
        Venue(venue_name="Echo Stage", address="8 Art District", city="Shanghai", room="Live House", capacity=80),
        Venue(venue_name="Garden Room", address="5 Park Lane", city="Hangzhou", room="Garden Terrace", capacity=60),
        Venue(venue_name="Studio 9", address="99 Tech Park", city="Shenzhen", room="Lab Room", capacity=40),
    ]
    db.session.add_all(venues)
    db.session.flush()

    # ---- 3. Artists ----
    artists = [
        Artist(first_name="The Blue River", second_name="Quartet", artist_type="Band", music_genre="Jazz", bio="Four-piece jazz ensemble."),
        Artist(first_name="Campus", second_name="Bands", artist_type="Group", music_genre="Campus Festival", bio="Student bands from top universities."),
        Artist(first_name="Indie", second_name="Rockers", artist_type="Band", music_genre="Rock", bio="Local indie rock group."),
        Artist(first_name="Acoustic", second_name="Duo", artist_type="Duo", music_genre="Acoustic", bio="Intimate acoustic performances."),
    ]
    db.session.add_all(artists)
    db.session.flush()

    # ---- 4. Events ----
    events = [
        MusicEvent(
            event_title="Riverside Jazz Night",
            description="A warm live-jazz session with skyline views, food stalls and 38 tickets still available.",
            start_time=now + timedelta(days=11, hours=19),
            end_time=now + timedelta(days=11, hours=22),
            capacity=100,
            age_restriction=12,
            event_status="Open",
            music_genre="Jazz",
            organizer_id=organizer.organizer_id,
            venue_id=venues[0].venue_id,
        ),
        MusicEvent(
            event_title="Campus Music Festival",
            description="Student bands, outdoor market energy and a summer-night crowd.",
            start_time=now + timedelta(days=13, hours=16),
            end_time=now + timedelta(days=13, hours=21),
            capacity=500,
            age_restriction=0,
            event_status="Open",
            music_genre="Campus Festival",
            organizer_id=organizer.organizer_id,
            venue_id=venues[1].venue_id,
        ),
        MusicEvent(
            event_title="Indie Rock Live",
            description="Local indie bands, a packed stage and an energetic live-house atmosphere.",
            start_time=now + timedelta(days=15, hours=20),
            end_time=now + timedelta(days=15, hours=23),
            capacity=80,
            age_restriction=16,
            event_status="Sold Out",
            music_genre="Rock",
            organizer_id=organizer.organizer_id,
            venue_id=venues[2].venue_id,
        ),
        MusicEvent(
            event_title="Acoustic Sunset Session",
            description="An intimate acoustic weekend session in a garden setting.",
            start_time=now + timedelta(days=17, hours=17, minutes=30),
            end_time=now + timedelta(days=17, hours=20),
            capacity=60,
            age_restriction=0,
            event_status="Cancelled",
            music_genre="Acoustic",
            organizer_id=organizer.organizer_id,
            venue_id=venues[3].venue_id,
        ),
        MusicEvent(
            event_title="Electronic Night Lab",
            description="An experimental electronic music night with cutting-edge sound design.",
            start_time=now - timedelta(days=11, hours=21),
            end_time=now - timedelta(days=11, hours=23, minutes=59),
            capacity=40,
            age_restriction=18,
            event_status="Inactive",
            music_genre="Concert",
            organizer_id=organizer.organizer_id,
            venue_id=venues[4].venue_id,
        ),
    ]
    db.session.add_all(events)
    db.session.flush()

    # ---- 5. Link Artists to Events ----
    events[0].artists.append(artists[0])
    events[1].artists.append(artists[1])
    events[2].artists.append(artists[2])
    events[3].artists.append(artists[3])
    events[4].artists.append(artists[1])

    # ---- 6. Registrations ----
    reg1 = Registration(
        participant_id=participant.participant_id,
        event_id=events[0].event_id,
    )
    db.session.add(reg1)
    db.session.flush()
    reg1.confirmRegistration()
    reg2 = Registration(
        participant_id=participant.participant_id,
        event_id=events[1].event_id,
    )
    db.session.add(reg2)
    db.session.flush()
    reg2.confirmRegistration()

    # ---- 7. Tickets & Payments ----
    t1 = Ticket(
        ticket_type="standard", price=32.00, qr_code="SW-TKT-001",
        registration_id=reg1.registration_id,
    )
    t2 = Ticket(
        ticket_type="free", price=0.00, qr_code="SW-TKT-002",
        registration_id=reg2.registration_id,
    )
    p1 = Payment(
        amount=32.00, payment_method="card",
        payment_time=now - timedelta(days=5),
        payment_status="Paid",
        registration_id=reg1.registration_id,
    )

    db.session.add_all([t1, t2, p1])
    db.session.commit()

    # ---- 8. Comments ----
    comments = [
        Comment(
            content="Absolutely loved the atmosphere! The riverside setting was magical.",
            user_id=participant.user_id,
            event_id=events[0].event_id,
        ),
        Comment(
            content="Great lineup this year. Can't wait for the next edition!",
            user_id=participant.user_id,
            event_id=events[1].event_id,
        ),
        Comment(
            content="The jazz quartet was incredible. Will definitely come again.",
            user_id=organizer.user_id,
            event_id=events[0].event_id,
        ),
    ]
    db.session.add_all(comments)
    db.session.commit()

    print("Seed data inserted successfully!")
    print(f"  Users: 1 organizer + 1 participant")
    print(f"  Venues: {len(venues)}")
    print(f"  Artists: {len(artists)}")
    print(f"  Events: {len(events)}")
    print(f"  Registrations: 2")
    print(f"  Comments: {len(comments)}")
