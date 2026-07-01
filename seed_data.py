from datetime import datetime, timedelta
from decimal import Decimal

from werkzeug.security import generate_password_hash

from app import create_app
from app.domain.value_objects import (
    Address,
    AgeRestriction,
    ArtistType,
    Capacity,
    City,
    ContactNumber,
    DateTime,
    Email,
    EventStatus,
    EventTitle,
    Money,
    MusicGenre,
    Name,
    Nickname,
    OrganizationName,
    PasswordHash,
    PaymentMethod,
    PaymentStatus,
    QRCode,
    Room,
    Text100,
    Text200,
    Text500,
    TicketType,
    VenueName,
)
from app.extensions import db
from app.models import Organizer, Participant, MusicEvent, Venue, Artist, Registration, Ticket, Payment, Comment, Announcement

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    now = datetime.now()

    # ---- 1. Users ----
    organizer = Organizer(
        nickname=Nickname("music_live"),
        email=Email("organizer@soundwave.com"),
        password_hash=PasswordHash(generate_password_hash("123456")),
        contact_number=ContactNumber("+86 138 0000 1111"),
        street_address=Address("10 Music Street"),
        organization_name=OrganizationName("SoundWave Productions"),
        first_name=Name("David"),
        second_name=Name("Lee"),
        bio=Text100("Professional music event organizer."),
    )

    participant = Participant(
        nickname=Nickname("alexchen"),
        email=Email("alex@soundwave.com"),
        password_hash=PasswordHash(generate_password_hash("123456")),
        contact_number=ContactNumber("+86 138 0000 2222"),
        street_address=Address("88 Happy Road"),
        first_name=Name("Alex"),
        second_name=Name("Chen"),
    )

    db.session.add_all([organizer, participant])
    db.session.flush()

    # ---- 2. Venues ----
    venues = [
        Venue(venue_name=VenueName("Blue Hall"), address=Address("15 Riverside Ave"), city=City("Shanghai"), room=Room("Hall A"), capacity=Capacity(100)),
        Venue(venue_name=VenueName("Main Lawn"), address=Address("22 University Blvd"), city=City("Beijing"), room=Room("Outdoor Stage"), capacity=Capacity(500)),
        Venue(venue_name=VenueName("Echo Stage"), address=Address("8 Art District"), city=City("Shanghai"), room=Room("Live House"), capacity=Capacity(80)),
        Venue(venue_name=VenueName("Garden Room"), address=Address("5 Park Lane"), city=City("Hangzhou"), room=Room("Garden Terrace"), capacity=Capacity(60)),
        Venue(venue_name=VenueName("Studio 9"), address=Address("99 Tech Park"), city=City("Shenzhen"), room=Room("Lab Room"), capacity=Capacity(40)),
    ]
    db.session.add_all(venues)
    db.session.flush()

    # ---- 3. Artists ----
    artists = [
        Artist(first_name=Name("BlueRiver"), second_name=Name("Quartet"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Jazz"), bio=Text100("Four-piece jazz ensemble.")),
        Artist(first_name=Name("Campus"), second_name=Name("Bands"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Campus Festival"), bio=Text100("Student bands from top universities.")),
        Artist(first_name=Name("Indie"), second_name=Name("Rockers"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Rock"), bio=Text100("Local indie rock group.")),
        Artist(first_name=Name("Acoustic"), second_name=Name("Duo"), artist_type=ArtistType("Duo"), music_genre=MusicGenre("Acoustic"), bio=Text100("Intimate acoustic performances.")),
    ]
    db.session.add_all(artists)
    db.session.flush()

    # ---- 4. Events ----
    events = [
        MusicEvent(
            event_title=EventTitle("Riverside Jazz Night"),
            description=Text200("A warm live-jazz session with skyline views, food stalls and 38 tickets still available."),
            start_time=DateTime(now + timedelta(days=11, hours=19)),
            end_time=DateTime(now + timedelta(days=11, hours=22)),
            capacity=Capacity(100),
            age_restriction=AgeRestriction(12),
            event_status=EventStatus("Open"),
            music_genre=MusicGenre("Jazz"),
            organizer_id=organizer.organizer_id,
            venue_id=venues[0].venue_id,
        ),
        MusicEvent(
            event_title=EventTitle("Campus Music Festival"),
            description=Text200("Student bands, outdoor market energy and a summer-night crowd."),
            start_time=DateTime(now + timedelta(days=13, hours=16)),
            end_time=DateTime(now + timedelta(days=13, hours=21)),
            capacity=Capacity(500),
            age_restriction=AgeRestriction(0),
            event_status=EventStatus("Open"),
            music_genre=MusicGenre("Campus Festival"),
            organizer_id=organizer.organizer_id,
            venue_id=venues[1].venue_id,
        ),
        MusicEvent(
            event_title=EventTitle("Indie Rock Live"),
            description=Text200("Local indie bands, a packed stage and an energetic live-house atmosphere."),
            start_time=DateTime(now + timedelta(days=15, hours=20)),
            end_time=DateTime(now + timedelta(days=15, hours=23)),
            capacity=Capacity(80),
            age_restriction=AgeRestriction(16),
            event_status=EventStatus("Sold Out"),
            music_genre=MusicGenre("Rock"),
            organizer_id=organizer.organizer_id,
            venue_id=venues[2].venue_id,
        ),
        MusicEvent(
            event_title=EventTitle("Acoustic Sunset Session"),
            description=Text200("An intimate acoustic weekend session in a garden setting."),
            start_time=DateTime(now + timedelta(days=17, hours=17, minutes=30)),
            end_time=DateTime(now + timedelta(days=17, hours=20)),
            capacity=Capacity(60),
            age_restriction=AgeRestriction(0),
            event_status=EventStatus("Cancelled"),
            music_genre=MusicGenre("Acoustic"),
            organizer_id=organizer.organizer_id,
            venue_id=venues[3].venue_id,
        ),
        MusicEvent(
            event_title=EventTitle("Electronic Night Lab"),
            description=Text200("An experimental electronic music night with cutting-edge sound design."),
            start_time=DateTime(now - timedelta(days=11, hours=21)),
            end_time=DateTime(now - timedelta(days=11, hours=23, minutes=59)),
            capacity=Capacity(40),
            age_restriction=AgeRestriction(18),
            event_status=EventStatus("Inactive"),
            music_genre=MusicGenre("Concert"),
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
        ticket_type=TicketType("standard"), price=Money(Decimal("32.00")), qr_code=QRCode("SW-TKT-001"),
        registration_id=reg1.registration_id,
    )
    t2 = Ticket(
        ticket_type=TicketType("free"), price=Money(Decimal("0.00")), qr_code=QRCode("SW-TKT-002"),
        registration_id=reg2.registration_id,
    )
    p1 = Payment(
        amount=Money(Decimal("32.00")), payment_method=PaymentMethod("card"),
        payment_time=DateTime(now - timedelta(days=5)),
        payment_status=PaymentStatus("Paid"),
        registration_id=reg1.registration_id,
    )

    db.session.add_all([t1, t2, p1])
    db.session.commit()

    # ---- 8. Comments ----
    comments = [
        Comment(
            content=Text500("Absolutely loved the atmosphere! The riverside setting was magical."),
            user_id=participant.user_id,
            event_id=events[0].event_id,
        ),
        Comment(
            content=Text500("Great lineup this year. Can't wait for the next edition!"),
            user_id=participant.user_id,
            event_id=events[1].event_id,
        ),
        Comment(
            content=Text500("The jazz quartet was incredible. Will definitely come again."),
            user_id=organizer.user_id,
            event_id=events[0].event_id,
        ),
    ]
    db.session.add_all(comments)
    db.session.flush()

    # ---- 9. Announcements ----
    announcement = Announcement(
        content=Text500("Welcome to Riverside Jazz Night! Doors open at 6:30 PM. Please have your QR code ready for check-in."),
        event_id=events[0].event_id,
    )
    db.session.add(announcement)
    db.session.commit()

    print("Seed data inserted successfully!")
    print(f"  Users: 1 organizer + 1 participant")
    print(f"  Venues: {len(venues)}")
    print(f"  Artists: {len(artists)}")
    print(f"  Events: {len(events)}")
    print(f"  Registrations: 2")
    print(f"  Comments: {len(comments)}")
    print(f"  Announcements: 1")
