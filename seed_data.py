from datetime import datetime, timedelta
from decimal import Decimal

from app.extensions import bcrypt

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

    # ============================================================
    # 1. Users -- 4 Organizers + 2 Participants
    # ============================================================
    organizer1 = Organizer(
        nickname=Nickname("music_live"),
        email=Email("organizer@soundwave.com"),
        password_hash=PasswordHash(bcrypt.generate_password_hash("123456").decode("utf-8")),
        contact_number=ContactNumber("+86 138 0000 1111"),
        street_address=Address("10 Music Street"),
        organization_name=OrganizationName("SoundWave Productions"),
        first_name=Name("David"),
        second_name=Name("Lee"),
        bio=Text100("Professional music event organizer."),
    )

    organizer2 = Organizer(
        nickname=Nickname("melody_sarah"),
        email=Email("sarah@soundwave.com"),
        password_hash=PasswordHash(bcrypt.generate_password_hash("123456").decode("utf-8")),
        contact_number=ContactNumber("+86 139 0000 2222"),
        street_address=Address("25 Harmony Lane"),
        organization_name=OrganizationName("Melody Makers Inc."),
        first_name=Name("Sarah"),
        second_name=Name("Wang"),
        bio=Text100("Bringing the best live music experiences to the city."),
    )

    organizer3 = Organizer(
        nickname=Nickname("rhythm_mike"),
        email=Email("mike@soundwave.com"),
        password_hash=PasswordHash(bcrypt.generate_password_hash("123456").decode("utf-8")),
        contact_number=ContactNumber("+86 137 0000 3333"),
        street_address=Address("88 Beat Street"),
        organization_name=OrganizationName("Rhythm Nation"),
        first_name=Name("Mike"),
        second_name=Name("Zhang"),
        bio=Text100("Dedicated to discovering and promoting emerging artists."),
    )

    organizer4 = Organizer(
        nickname=Nickname("harmony_lisa"),
        email=Email("lisa@soundwave.com"),
        password_hash=PasswordHash(bcrypt.generate_password_hash("123456").decode("utf-8")),
        contact_number=ContactNumber("+86 136 0000 4444"),
        street_address=Address("42 Melody Avenue"),
        organization_name=OrganizationName("Harmony Events Co."),
        first_name=Name("Lisa"),
        second_name=Name("Chen"),
        bio=Text100("Curating intimate acoustic and indie music gatherings."),
    )

    participant1 = Participant(
        nickname=Nickname("alexchen"),
        email=Email("alex@soundwave.com"),
        password_hash=PasswordHash(bcrypt.generate_password_hash("123456").decode("utf-8")),
        contact_number=ContactNumber("+86 138 0000 2222"),
        street_address=Address("88 Happy Road"),
        first_name=Name("Alex"),
        second_name=Name("Chen"),
    )

    participant2 = Participant(
        nickname=Nickname("emma_wu"),
        email=Email("emma@soundwave.com"),
        password_hash=PasswordHash(bcrypt.generate_password_hash("123456").decode("utf-8")),
        contact_number=ContactNumber("+86 135 0000 5555"),
        street_address=Address("56 Garden Street"),
        first_name=Name("Emma"),
        second_name=Name("Wu"),
    )

    organizers = [organizer1, organizer2, organizer3, organizer4]
    participants = [participant1, participant2]

    db.session.add_all(organizers + participants)
    db.session.flush()

    # ============================================================
    # 2. Venues -- 10 venues
    # ============================================================
    venues = [
        Venue(venue_name=VenueName("Blue Hall"), address=Address("15 Riverside Ave"), city=City("Shanghai"), room=Room("Hall A"), capacity=Capacity(100)),
        Venue(venue_name=VenueName("Main Lawn"), address=Address("22 University Blvd"), city=City("Beijing"), room=Room("Outdoor Stage"), capacity=Capacity(500)),
        Venue(venue_name=VenueName("Echo Stage"), address=Address("8 Art District"), city=City("Shanghai"), room=Room("Live House"), capacity=Capacity(80)),
        Venue(venue_name=VenueName("Garden Room"), address=Address("5 Park Lane"), city=City("Hangzhou"), room=Room("Garden Terrace"), capacity=Capacity(60)),
        Venue(venue_name=VenueName("Studio 9"), address=Address("99 Tech Park"), city=City("Shenzhen"), room=Room("Lab Room"), capacity=Capacity(40)),
        Venue(venue_name=VenueName("Sunset Arena"), address=Address("100 Coastal Road"), city=City("Shanghai"), room=Room("Main Arena"), capacity=Capacity(800)),
        Venue(venue_name=VenueName("Crystal Palace"), address=Address("33 Diamond Blvd"), city=City("Beijing"), room=Room("Grand Ballroom"), capacity=Capacity(300)),
        Venue(venue_name=VenueName("The Underground"), address=Address("7 Basement Lane"), city=City("Guangzhou"), room=Room("Cellar Stage"), capacity=Capacity(50)),
        Venue(venue_name=VenueName("Harbor Deck"), address=Address("12 Pier Street"), city=City("Shanghai"), room=Room("Open Deck"), capacity=Capacity(200)),
        Venue(venue_name=VenueName("Moonlight Theater"), address=Address("20 Star Avenue"), city=City("Beijing"), room=Room("Main Theater"), capacity=Capacity(150)),
    ]
    db.session.add_all(venues)
    db.session.flush()

    # ============================================================
    # 3. Artists -- 20 artists across genres
    # ============================================================
    artists = [
        # Jazz artists
        Artist(first_name=Name("BlueRiver"), second_name=Name("Quartet"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Jazz"), bio=Text100("Four-piece jazz ensemble.")),
        Artist(first_name=Name("Smooth"), second_name=Name("Trio"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Jazz"), bio=Text100("Classic jazz with a modern smooth twist.")),
        Artist(first_name=Name("Night"), second_name=Name("Saxophone"), artist_type=ArtistType("Solo"), music_genre=MusicGenre("Jazz"), bio=Text100("Solo saxophonist blending jazz and ambient.")),
        Artist(first_name=Name("Swing"), second_name=Name("Collective"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Jazz"), bio=Text100("Big band swing jazz revival.")),

        # Rock artists
        Artist(first_name=Name("Indie"), second_name=Name("Rockers"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Rock"), bio=Text100("Local indie rock group.")),
        Artist(first_name=Name("Thunder"), second_name=Name("Volt"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Rock"), bio=Text100("High-energy hard rock band.")),
        Artist(first_name=Name("Neon"), second_name=Name("Rebels"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Rock"), bio=Text100("Punk-pop trio shaking up the scene.")),
        Artist(first_name=Name("Shadow"), second_name=Name("Drive"), artist_type=ArtistType("Duo"), music_genre=MusicGenre("Rock"), bio=Text100("Garage rock duo with raw gritty sound.")),

        # Campus Festival artists
        Artist(first_name=Name("Campus"), second_name=Name("Bands"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Campus Festival"), bio=Text100("Student bands from top universities.")),
        Artist(first_name=Name("Youth"), second_name=Name("Wave"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Campus Festival"), bio=Text100("University pop-rock collective.")),
        Artist(first_name=Name("Dormitory"), second_name=Name("Echoes"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Campus Festival"), bio=Text100("Dorm-room acoustic project gone big.")),
        Artist(first_name=Name("Graduation"), second_name=Name("Anthem"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Campus Festival"), bio=Text100("Senior year band celebrating campus life.")),

        # Acoustic artists
        Artist(first_name=Name("Acoustic"), second_name=Name("Duo"), artist_type=ArtistType("Duo"), music_genre=MusicGenre("Acoustic"), bio=Text100("Intimate acoustic performances.")),
        Artist(first_name=Name("Fingerstyle"), second_name=Name("Li"), artist_type=ArtistType("Solo"), music_genre=MusicGenre("Acoustic"), bio=Text100("Solo fingerstyle guitar virtuoso.")),
        Artist(first_name=Name("Wood"), second_name=Name("Strings"), artist_type=ArtistType("Duo"), music_genre=MusicGenre("Acoustic"), bio=Text100("Guitar and violin acoustic harmony.")),
        Artist(first_name=Name("Fireside"), second_name=Name("Folk"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Acoustic"), bio=Text100("Warm folk-acoustic storytelling.")),

        # Concert artists
        Artist(first_name=Name("Synth"), second_name=Name("Horizon"), artist_type=ArtistType("Band"), music_genre=MusicGenre("Concert"), bio=Text100("Electronic-synth concert experience.")),
        Artist(first_name=Name("Orchestra"), second_name=Name("Nova"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Concert"), bio=Text100("Full symphony orchestra with modern flair.")),
        Artist(first_name=Name("DJ"), second_name=Name("Pulse"), artist_type=ArtistType("Solo"), music_genre=MusicGenre("Concert"), bio=Text100("EDM DJ bringing the festival energy.")),
        Artist(first_name=Name("Vocal"), second_name=Name("Ensemble"), artist_type=ArtistType("Group"), music_genre=MusicGenre("Concert"), bio=Text100("Choral ensemble performing contemporary pieces.")),
    ]
    db.session.add_all(artists)
    db.session.flush()

    # Shorthand for artists
    a = artists  # 0-3 Jazz, 4-7 Rock, 8-11 Campus, 12-15 Acoustic, 16-19 Concert

    # ============================================================
    # 4. Events -- ~10 per genre, ~50 total
    # ============================================================
    # Helper: pick an organizer round-robin
    def org(i):
        return organizers[i % len(organizers)]

    events_data = []

    # --- JAZZ events (10) ---
    jazz_events = [
        (org(0), venues[0], "Riverside Jazz Night", "A warm live-jazz session with skyline views and food stalls.", 19, 22, 100, 12, "Open", 11),
        (org(1), venues[2], "Sunset Smooth Jazz", "Smooth jazz under the sunset with cocktail pairing.", 18, 21, 80, 16, "Open", 14),
        (org(2), venues[3], "Jazz in the Garden", "An intimate garden jazz evening with acoustic ambiance.", 17, 20, 60, 0, "Open", 18),
        (org(3), venues[8], "Harbor Jazz Cruise", "Jazz night on the harbor deck with sea breeze.", 19, 22, 200, 18, "Open", 20),
        (org(0), venues[9], "Moonlight Jazz Soiree", "Elegant jazz under the moonlight with candlelit tables.", 20, 23, 150, 21, "Open", 25),
        (org(1), venues[0], "Swing into Spring", "Big band swing revival night with dance floor open.", 18, 22, 100, 12, "Sold Out", 8),
        (org(2), venues[2], "Late Night Jazz Jam", "Open jam session for jazz musicians and enthusiasts.", 21, 23, 80, 18, "Open", 15),
        (org(3), venues[7], "Basement Jazz Underground", "Underground jazz in a cozy cellar setting.", 19, 21, 50, 16, "draft", 0),
        (org(0), venues[3], "Jazz Brunch Special", "Sunday jazz brunch with live trio and mimosas.", 10, 13, 60, 0, "Cancelled", 0),
        (org(1), venues[9], "Jazz Legends Tribute", "A past tribute concert to jazz legends.", 20, 23, 150, 12, "Inactive", -10),
    ]

    # --- ROCK events (10) ---
    rock_events = [
        (org(0), venues[2], "Indie Rock Live", "Local indie bands with a packed live-house atmosphere.", 20, 23, 80, 16, "Open", 15),
        (org(1), venues[5], "Thunder Fest 2026", "Hard rock festival with multiple bands on the arena stage.", 18, 23, 800, 16, "Open", 21),
        (org(2), venues[7], "Punk Night Rebellion", "Loud, fast, and unapologetic punk rock in the basement.", 20, 23, 50, 18, "Open", 12),
        (org(3), venues[6], "Rock the Palace", "Rock bands take over the grand ballroom.", 19, 22, 300, 16, "Open", 18),
        (org(0), venues[8], "Harbor Rock Sea Breeze", "Rock by the water with ocean views and cold drinks.", 18, 21, 200, 14, "Open", 16),
        (org(1), venues[2], "Garage Rock Revival", "Raw and gritty garage rock duo live performance.", 20, 22, 80, 16, "Sold Out", 7),
        (org(2), venues[9], "Neon Rebels Live", "Punk-pop trio headlining a theater show.", 19, 22, 150, 12, "Open", 19),
        (org(3), venues[5], "Summer Rock Countdown", "Countdown to summer with rock anthems all night.", 17, 23, 800, 0, "Open", 28),
        (org(0), venues[7], "Emo Night Rewind", "A nostalgic emo and pop-punk throwback party.", 21, 23, 50, 18, "draft", 0),
        (org(1), venues[6], "Rock Legends Past", "A past tribute concert for classic rock legends.", 19, 23, 300, 14, "Inactive", -14),
    ]

    # --- CAMPUS FESTIVAL events (10) ---
    campus_events = [
        (org(0), venues[1], "Campus Music Festival", "Student bands and outdoor market energy for a summer night.", 16, 21, 500, 0, "Open", 13),
        (org(1), venues[5], "Spring Campus Bash", "University-wide spring celebration with live performances.", 14, 20, 800, 0, "Open", 20),
        (org(2), venues[1], "Freshman Welcome Fest", "Welcome new students with music and campus spirit.", 15, 19, 500, 0, "Open", 25),
        (org(3), venues[1], "Graduation Music Night", "Celebrate graduation with the best campus bands.", 17, 22, 500, 0, "Open", 30),
        (org(0), venues[5], "Inter-University Battle", "Top student bands from five universities compete.", 13, 18, 800, 0, "Open", 15),
        (org(1), venues[1], "Dorm Jam 2026", "Dormitory Echoes headline the biggest campus jam.", 18, 22, 500, 0, "Sold Out", 9),
        (org(2), venues[5], "Campus Acoustic Night", "Unplugged sessions under the stars on the lawn.", 17, 20, 800, 0, "Open", 18),
        (org(3), venues[1], "Autumn Campus Fair", "Music, food stalls, and games at the autumn fair.", 12, 18, 500, 0, "Open", 35),
        (org(0), venues[5], "Campus DJ Clash", "Student DJs compete for the campus crown.", 19, 23, 800, 16, "Cancelled", 0),
        (org(1), venues[1], "Last Semester Sendoff", "End-of-year sendoff concert for outgoing students.", 17, 22, 500, 0, "Inactive", -30),
    ]

    # --- ACOUSTIC events (10) ---
    acoustic_events = [
        (org(0), venues[3], "Acoustic Sunset Session", "An intimate acoustic weekend session in a garden.", 17, 20, 60, 0, "Cancelled", 17),
        (org(1), venues[4], "Fingerstyle Guitar Night", "Solo fingerstyle guitar master Li performs live.", 19, 21, 40, 12, "Open", 10),
        (org(2), venues[7], "Candlelit Acoustic Eve", "Soft acoustic melodies by candlelight in a cozy cellar.", 18, 20, 50, 0, "Open", 13),
        (org(3), venues[3], "Wood Strings Harmony", "Guitar and violin acoustic duo in the garden.", 16, 19, 60, 8, "Open", 16),
        (org(0), venues[8], "Harbor Acoustic Breeze", "Gentle acoustic tunes with harbor sunset views.", 17, 20, 200, 0, "Open", 22),
        (org(1), venues[9], "Fireside Folk Stories", "Warm folk-acoustic storytelling in the theater.", 19, 21, 150, 10, "Open", 14),
        (org(2), venues[4], "Lo-Fi Acoustic Lab", "Experimental acoustic sounds in an intimate space.", 20, 22, 40, 16, "Sold Out", 5),
        (org(3), venues[3], "Morning Acoustic Yoga", "Start the day with acoustic music and yoga in the garden.", 8, 10, 60, 0, "Open", 8),
        (org(0), venues[7], "Acoustic Whiskey Night", "Acoustic tunes paired with fine whiskey tasting.", 20, 23, 50, 21, "draft", 0),
        (org(1), venues[9], "Folk Memories Concert", "A past acoustic folk concert of timeless classics.", 18, 21, 150, 8, "Inactive", -21),
    ]

    # --- CONCERT events (10) ---
    concert_events = [
        (org(0), venues[4], "Electronic Night Lab", "Experimental electronic music with cutting-edge sound.", 21, 23, 40, 18, "Inactive", -11),
        (org(1), venues[5], "Symphony Under Stars", "Full orchestra performing classical and modern pieces.", 19, 22, 800, 8, "Open", 17),
        (org(2), venues[6], "Crystal Gala Concert", "Grand ballroom concert with choral ensemble.", 18, 21, 300, 12, "Open", 19),
        (org(3), venues[8], "Harbor EDM Night", "DJ Pulse brings electronic energy to the harbor.", 20, 23, 200, 18, "Open", 15),
        (org(0), venues[5], "Synth Horizon Live", "Electronic-synth band in a massive arena spectacle.", 19, 22, 800, 14, "Open", 22),
        (org(1), venues[9], "Vocal Ensemble Evening", "Contemporary choral pieces in a beautiful theater.", 18, 20, 150, 6, "Open", 12),
        (org(2), venues[6], "New Year Concert Gala", "A sold-out New Year celebration concert.", 20, 23, 300, 12, "Sold Out", 4),
        (org(3), venues[5], "Orchestra Nova Premier", "Symphony orchestra premiering new compositions.", 19, 21, 800, 10, "Open", 24),
        (org(0), venues[4], "Ambient Sound Lab", "Immersive ambient electronic soundscape experience.", 20, 22, 40, 16, "draft", 0),
        (org(1), venues[8], "Summer Concert Finale", "A past grand finale summer harbor concert.", 19, 23, 200, 12, "Inactive", -18),
    ]

    # Build event objects
    all_event_specs = jazz_events + rock_events + campus_events + acoustic_events + concert_events
    events = []

    for org_obj, venue, title, desc, start_h, end_h, cap, age, status, day_offset in all_event_specs:
        e = MusicEvent(
            event_title=EventTitle(title),
            description=Text200(desc),
            start_time=DateTime(now + timedelta(days=day_offset, hours=start_h)),
            end_time=DateTime(now + timedelta(days=day_offset, hours=end_h)),
            capacity=Capacity(cap),
            age_restriction=AgeRestriction(age),
            event_status=EventStatus(status),
            music_genre=MusicGenre(org_obj.events[0].music_genre.value if hasattr(org_obj, 'events') and org_obj.events else "Jazz") if isinstance(org_obj, Organizer) else MusicGenre("Jazz"),
            organizer_id=org_obj.organizer_id,
            venue_id=venue.venue_id,
        )
        events.append(e)

    # We need to set the music_genre properly for each group
    genre_map = {
        "jazz": "Jazz",
        "rock": "Rock",
        "campus": "Campus Festival",
        "acoustic": "Acoustic",
        "concert": "Concert",
    }

    # Rebuild events with proper genre assignment
    events = []

    def add_events(specs, genre):
        for org_obj, venue, title, desc, start_h, end_h, cap, age, status, day_offset in specs:
            e = MusicEvent(
                event_title=EventTitle(title),
                description=Text200(desc),
                start_time=DateTime(now + timedelta(days=day_offset, hours=start_h)),
                end_time=DateTime(now + timedelta(days=day_offset, hours=end_h)),
                capacity=Capacity(cap),
                age_restriction=AgeRestriction(age),
                event_status=EventStatus(status),
                music_genre=MusicGenre(genre),
                organizer_id=org_obj.organizer_id,
                venue_id=venue.venue_id,
            )
            events.append(e)

    add_events(jazz_events, "Jazz")
    add_events(rock_events, "Rock")
    add_events(campus_events, "Campus Festival")
    add_events(acoustic_events, "Acoustic")
    add_events(concert_events, "Concert")

    db.session.add_all(events)
    db.session.flush()

    # ============================================================
    # 5. Link Artists to Events
    # ============================================================
    # Map events by genre
    jazz_evs = events[0:10]
    rock_evs = events[10:20]
    campus_evs = events[20:30]
    acoustic_evs = events[30:40]
    concert_evs = events[40:50]

    # Jazz: link each jazz event to 1-2 jazz artists (a[0]-a[3])
    for i, ev in enumerate(jazz_evs):
        ev.artists.append(a[i % 4])
        if i % 3 == 0:
            ev.artists.append(a[(i + 1) % 4])

    # Rock: link each rock event to 1-2 rock artists (a[4]-a[7])
    for i, ev in enumerate(rock_evs):
        ev.artists.append(a[4 + i % 4])
        if i % 3 == 0:
            ev.artists.append(a[4 + (i + 1) % 4])

    # Campus: link each campus event to 1-2 campus artists (a[8]-a[11])
    for i, ev in enumerate(campus_evs):
        ev.artists.append(a[8 + i % 4])
        if i % 3 == 0:
            ev.artists.append(a[8 + (i + 1) % 4])

    # Acoustic: link each acoustic event to 1-2 acoustic artists (a[12]-a[15])
    for i, ev in enumerate(acoustic_evs):
        ev.artists.append(a[12 + i % 4])
        if i % 3 == 0:
            ev.artists.append(a[12 + (i + 1) % 4])

    # Concert: link each concert event to 1-2 concert artists (a[16]-a[19])
    for i, ev in enumerate(concert_evs):
        ev.artists.append(a[16 + i % 4])
        if i % 3 == 0:
            ev.artists.append(a[16 + (i + 1) % 4])

    # ============================================================
    # 6. Registrations -- spread across participants and events
    # ============================================================
    registrations = []

    # Register participant1 for first 8 open events across genres
    reg_targets = [e for e in events if str(e.event_status) in ("Open",)][:8]
    for ev in reg_targets:
        reg = Registration(
            participant_id=participant1.participant_id,
            event_id=ev.event_id,
        )
        db.session.add(reg)
        db.session.flush()
        reg.confirmRegistration()
        registrations.append(reg)

    # Register participant2 for a different set of open events
    reg_targets2 = [e for e in events if str(e.event_status) in ("Open",)][8:16]
    for ev in reg_targets2:
        reg = Registration(
            participant_id=participant2.participant_id,
            event_id=ev.event_id,
        )
        db.session.add(reg)
        db.session.flush()
        reg.confirmRegistration()
        registrations.append(reg)

    # Also register participant1 for the Sold Out events
    sold_out_evs = [e for e in events if str(e.event_status) == "Sold Out"]
    for ev in sold_out_evs:
        reg = Registration(
            participant_id=participant2.participant_id,
            event_id=ev.event_id,
        )
        db.session.add(reg)
        db.session.flush()
        reg.confirmRegistration()
        registrations.append(reg)

    # ============================================================
    # 7. Tickets & Payments
    # ============================================================
    ticket_types = ["standard", "vip", "free"]
    payment_methods = ["card", "paypal", "bank_transfer"]
    ticket_counter = 1

    for reg in registrations:
        ev = [e for e in events if e.event_id == reg.event_id][0]
        ttype = ticket_types[ticket_counter % len(ticket_types)]
        price = Decimal("0.00") if ttype == "free" else Decimal(f"{15 + (ticket_counter % 6) * 5}.00")
        t = Ticket(
            ticket_type=TicketType(ttype),
            price=Money(price),
            qr_code=QRCode(f"SW-TKT-{ticket_counter:03d}"),
            registration_id=reg.registration_id,
        )
        db.session.add(t)

        if price > 0:
            p = Payment(
                amount=Money(price),
                payment_method=PaymentMethod(payment_methods[ticket_counter % len(payment_methods)]),
                payment_time=DateTime(now - timedelta(days=ticket_counter % 30)),
                payment_status=PaymentStatus("Paid"),
                registration_id=reg.registration_id,
            )
            db.session.add(p)

        ticket_counter += 1

    db.session.commit()

    # ============================================================
    # 8. Comments
    # ============================================================
    comments_data = [
        ("Absolutely loved the atmosphere! The riverside setting was magical.", participant1.user_id, events[0].event_id),
        ("Great lineup this year. Can't wait for the next edition!", participant1.user_id, events[20].event_id),
        ("The jazz quartet was incredible. Will definitely come again.", organizer1.user_id, events[0].event_id),
        ("Best rock concert I have been to in years. Amazing energy!", participant2.user_id, events[10].event_id),
        ("The campus festival was so much fun. Great student talent.", participant1.user_id, events[22].event_id),
        ("Loved the acoustic session. So peaceful and beautiful.", participant2.user_id, events[30].event_id),
        ("Symphony orchestra was world-class. Stunning performance.", participant1.user_id, events[41].event_id),
        ("Harbor jazz night was the perfect date night. Highly recommend!", participant2.user_id, events[3].event_id),
        ("Thunder Fest was absolutely insane! Can't wait for next year.", participant1.user_id, events[11].event_id),
        ("The fingerstyle guitar performance moved me to tears. Incredible talent.", participant2.user_id, events[31].event_id),
        ("Great venue, great sound, great night. Well organized!", participant1.user_id, events[13].event_id),
        ("Candlelit acoustic evening was magical. Will bring more friends next time.", participant2.user_id, events[32].event_id),
    ]
    for content, uid, eid in comments_data:
        db.session.add(Comment(content=Text500(content), user_id=uid, event_id=eid))

    db.session.flush()

    # ============================================================
    # 9. Announcements
    # ============================================================
    announcements_data = [
        ("Welcome to Riverside Jazz Night! Doors open at 6:30 PM. Please have your QR code ready for check-in.", events[0].event_id),
        ("Important: Thunder Fest gates open at 5 PM. Early arrival recommended for best spots.", events[11].event_id),
        ("Campus Music Festival update: Food stalls and merchandise booths open from 2 PM.", events[20].event_id),
        ("Acoustic Sunset Session: Please bring your own blankets for garden seating.", events[30].event_id),
        ("Symphony Under Stars: Dress code is smart casual. No flash photography during performance.", events[41].event_id),
        ("Harbor Jazz Cruise update: Boarding starts at 6 PM. Don't miss the sunset!", events[3].event_id),
        ("Spring Campus Bash: Free shuttle buses available from all university gates.", events[21].event_id),
        ("Candlelit Acoustic Eve: Limited seats remaining. Please arrive 15 minutes early.", events[32].event_id),
    ]
    for content, eid in announcements_data:
        db.session.add(Announcement(content=Text500(content), event_id=eid))

    db.session.commit()

    # ============================================================
    # Summary
    # ============================================================
    print("Seed data inserted successfully!")
    print(f"  Organizers: {len(organizers)}")
    print(f"  Participants: {len(participants)}")
    print(f"  Venues: {len(venues)}")
    print(f"  Artists: {len(artists)}")
    print(f"  Events: {len(events)}")
    print(f"    - Jazz: {len(jazz_evs)}")
    print(f"    - Rock: {len(rock_evs)}")
    print(f"    - Campus Festival: {len(campus_evs)}")
    print(f"    - Acoustic: {len(acoustic_evs)}")
    print(f"    - Concert: {len(concert_evs)}")
    print(f"  Registrations: {len(registrations)}")
    print(f"  Comments: {len(comments_data)}")
    print(f"  Announcements: {len(announcements_data)}")
