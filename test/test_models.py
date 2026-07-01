"""Tests for SQLAlchemy models."""

from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest

from app.domain.value_objects import (
    Address, AgeRestriction, ArtistType, Capacity, CheckInStatus,
    ContactNumber, DateTime, Email, EventStatus, EventTitle, Money,
    MusicGenre, Name, Nickname, PasswordHash, PaymentMethod,
    RegistrationStatus, Text100, Text200, TicketType, Text500
)
from app.extensions import db
from app.models.user import User
from app.models.participant import Participant
from app.models.organizer import Organizer
from app.models.admin import Admin
from app.models.music_event import MusicEvent
from app.models.venue import Venue
from app.models.artist import Artist
from app.models.registration import Registration
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.models.comment import Comment
from app.models.announcement import Announcement


# =============================================================================
# Helpers
# =============================================================================

def _create_venue(session):
    from app.domain.value_objects import VenueName, City, Room, Address
    v = Venue(
        venue_name=VenueName("Test Venue"),
        address=Address("123 Main St"),
        city=City("Brisbane"),
        room=Room("Main Hall"),
        capacity=Capacity(500),
    )
    session.add(v)
    session.commit()
    return v


_org_counter = 0


def _create_organizer(session, email=None):
    global _org_counter
    from werkzeug.security import generate_password_hash
    from app.domain.value_objects import OrganizationName
    _org_counter += 1
    pw_hash = generate_password_hash("password123")
    o = Organizer(
        nickname=Nickname(f"org_admin{_org_counter}"),
        email=Email(email or f"org{_org_counter}@test.com"),
        password_hash=PasswordHash(pw_hash),
        contact_number=ContactNumber(f"041111111{_org_counter % 10}"),
        street_address=Address(f"{_org_counter} Org Street"),
        first_name=Name("Org"),
        second_name=Name("Admin"),
        bio=Text100("Organizer bio"),
    )
    o.organization_name = OrganizationName(f"OrgCorp{_org_counter}")
    session.add(o)
    session.commit()
    return o


def _create_participant(session):
    from werkzeug.security import generate_password_hash
    pw_hash = generate_password_hash("password123")
    p = Participant(
        nickname=Nickname("testuser"),
        email=Email("user@test.com"),
        password_hash=PasswordHash(pw_hash),
        contact_number=ContactNumber("0412345678"),
        street_address=Address("123 User St"),
        first_name=Name("John"),
        second_name=Name("Doe"),
    )
    session.add(p)
    session.commit()
    return p


def _create_event(session, organizer, venue):
    now = datetime.now(timezone.utc)
    e = MusicEvent(
        event_title=EventTitle("Rock Concert"),
        description=Text200("A great rock concert"),
        start_time=DateTime(now + timedelta(days=7)),
        end_time=DateTime(now + timedelta(days=7, hours=3)),
        capacity=Capacity(200),
        age_restriction=AgeRestriction(18),
        event_status=EventStatus("Open"),
        music_genre=MusicGenre("Rock"),
        organizer_id=organizer.organizer_id,
        venue_id=venue.venue_id,
    )
    session.add(e)
    session.commit()
    return e


# =============================================================================
# User
# =============================================================================

class TestUser:
    def test_create_user(self, session):
        from werkzeug.security import generate_password_hash
        pw_hash = generate_password_hash("secret")
        u = User(
            nickname=Nickname("testnick"),
            email=Email("test@example.com"),
            password_hash=PasswordHash(pw_hash),
            contact_number=ContactNumber("0400000000"),
            street_address=Address("1 Test St"),
        )
        session.add(u)
        session.commit()
        assert u.user_id is not None
        assert str(u.nickname) == "testnick"
        assert str(u.email) == "test@example.com"

    def test_user_unique_email(self, session):
        from werkzeug.security import generate_password_hash
        pw_hash = generate_password_hash("secret")
        u1 = User(
            nickname=Nickname("user1"),
            email=Email("unique@example.com"),
            password_hash=PasswordHash(pw_hash),
        )
        session.add(u1)
        session.commit()

        u2 = User(
            nickname=Nickname("user2"),
            email=Email("unique@example.com"),
            password_hash=PasswordHash(pw_hash),
        )
        session.add(u2)
        with pytest.raises(Exception):
            session.commit()

    def test_user_login_success(self, session):
        from werkzeug.security import generate_password_hash
        pw_hash = generate_password_hash("mypassword")
        u = User(
            nickname=Nickname("loginuser"),
            email=Email("login@test.com"),
            password_hash=PasswordHash(pw_hash),
        )
        session.add(u)
        session.commit()

        assert u.login(Email("login@test.com"), "mypassword") is True

    def test_user_login_wrong_password(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("correct")
        u = User(
            nickname=Nickname("pwuser"),
            email=Email("pw@test.com"),
            password_hash=PasswordHash(pw),
        )
        session.add(u)
        session.commit()

        assert u.login(Email("pw@test.com"), "wrongpassword") is False

    def test_user_login_nonexistent_email(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u = User(
            nickname=Nickname("real"),
            email=Email("real@test.com"),
            password_hash=PasswordHash(pw),
        )
        session.add(u)
        session.commit()

        assert u.login(Email("nobody@test.com"), "pw") is False

    def test_user_logout(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u = User(nickname=Nickname("out"), email=Email("out@test.com"), password_hash=PasswordHash(pw))
        session.add(u)
        session.commit()
        assert u.logout() is True

    def test_user_signup_success(self, session):
        u = User()
        result = u.signup(Nickname("newuser"), Email("new@test.com"), "password123")
        assert result is True
        assert u.user_id is not None

    def test_user_signup_duplicate_email(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u1 = User(nickname=Nickname("first"), email=Email("dup@test.com"), password_hash=PasswordHash(pw))
        session.add(u1)
        session.commit()

        u2 = User()
        result = u2.signup(Nickname("second"), Email("dup@test.com"), "password")
        assert result is False

    def test_user_update_profile(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u = User(nickname=Nickname("oldnick"), email=Email("old@test.com"), password_hash=PasswordHash(pw))
        session.add(u)
        session.commit()

        result = u.updateProfile(Nickname("newnick"), Email("new@test.com"))
        assert result is True
        assert str(u.nickname) == "newnick"

    def test_user_get_id(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u = User(nickname=Nickname("idtest"), email=Email("id@test.com"), password_hash=PasswordHash(pw))
        session.add(u)
        session.commit()
        assert u.get_id() == str(u.user_id)

    def test_user_optional_fields_none(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u = User(
            nickname=Nickname("minuser"),
            email=Email("min@test.com"),
            password_hash=PasswordHash(pw),
        )
        session.add(u)
        session.commit()
        assert u.contact_number is None
        assert u.street_address is None

    def test_user_type_error_on_setter(self, session):
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash("pw")
        u = User(nickname=Nickname("typeuser"), email=Email("type@test.com"), password_hash=PasswordHash(pw))
        session.add(u)
        session.commit()
        with pytest.raises(TypeError):
            u.nickname = "not_a_nickname"
        with pytest.raises(TypeError):
            u.email = "not_an_email"


# =============================================================================
# Participant
# =============================================================================

class TestParticipant:
    def test_create_participant(self, session):
        p = _create_participant(session)
        assert p.participant_id is not None
        assert str(p.first_name) == "John"
        assert str(p.second_name) == "Doe"
        assert p.contact_number is not None
        assert p.street_address is not None

    def test_participant_inherits_user(self, session):
        p = _create_participant(session)
        assert isinstance(p, User)
        assert p.get_id() == str(p.participant_id)

    def test_browse_events(self, session):
        p = _create_participant(session)
        events = p.browseEvents()
        assert isinstance(events, list)

    def test_register_event(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        reg_id = p.registerEvent(e.event_id)
        assert reg_id > 0

    def test_cancel_registration(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        reg_id = p.registerEvent(e.event_id)

        result = p.cancelRegistration(reg_id)
        assert result is True

    def test_cancel_nonexistent_registration(self, session):
        p = _create_participant(session)
        result = p.cancelRegistration(99999)
        assert result is False

    def test_view_ticket_nonexistent(self, session):
        p = _create_participant(session)
        assert p.viewTicket(99999) is None

    def test_check_in(self, session):
        p = _create_participant(session)
        assert p.checkIn(1) is True


# =============================================================================
# Organizer
# =============================================================================

class TestOrganizer:
    def test_create_organizer(self, session):
        o = _create_organizer(session)
        assert str(o.organization_name).startswith("OrgCorp")

    def test_organizer_inherits_user(self, session):
        o = _create_organizer(session)
        assert isinstance(o, User)

    def test_create_event(self, session):
        o = _create_organizer(session)
        v = _create_venue(session)
        event_id = o.createEvent(
            title=EventTitle("New Event"),
            description=Text200("Description here"),
            start_time=DateTime(datetime(2026, 8, 1)),
            end_time=DateTime(datetime(2026, 8, 1, 3)),
            capacity=Capacity(100),
        )
        assert event_id > 0
        event = db.session.get(MusicEvent, event_id)
        assert event is not None
        assert str(event.event_title) == "New Event"

    def test_update_event(self, session):
        o = _create_organizer(session)
        v = _create_venue(session)
        event_id = o.createEvent(
            title=EventTitle("Original"),
            description=Text200("Original desc"),
            start_time=DateTime(datetime(2026, 9, 1)),
            end_time=DateTime(datetime(2026, 9, 1, 3)),
            capacity=Capacity(50),
        )
        result = o.updateEvent(event_id, event_title=EventTitle("Updated Title"))
        assert result is True
        event = db.session.get(MusicEvent, event_id)
        assert str(event.event_title) == "Updated Title"

    def test_update_event_not_owned(self, session):
        o1 = _create_organizer(session)
        o2_in_name_only = _create_organizer(session)
        v = _create_venue(session)
        event_id = o1.createEvent(
            title=EventTitle("Event1"),
            description=Text200("Desc"),
            start_time=DateTime(datetime(2026, 10, 1)),
            end_time=DateTime(datetime(2026, 10, 1, 3)),
            capacity=Capacity(50),
        )
        # o2 tries to update o1's event; should fail
        result = o2_in_name_only.updateEvent(event_id, event_title=EventTitle("Hacked"))
        assert result is False

    def test_cancel_event(self, session):
        o = _create_organizer(session)
        v = _create_venue(session)
        event_id = o.createEvent(
            title=EventTitle("ToCancel"),
            description=Text200("Will be cancelled"),
            start_time=DateTime(datetime(2026, 11, 1)),
            end_time=DateTime(datetime(2026, 11, 1, 3)),
            capacity=Capacity(30),
        )
        assert o.cancelEvent(event_id) is True
        event = db.session.get(MusicEvent, event_id)
        assert event.event_status == "Cancelled"

    def test_view_participants(self, session):
        o = _create_organizer(session)
        v = _create_venue(session)
        event_id = o.createEvent(
            title=EventTitle("Party"),
            description=Text200("Party time"),
            start_time=DateTime(datetime(2026, 12, 1)),
            end_time=DateTime(datetime(2026, 12, 1, 5)),
            capacity=Capacity(100),
        )
        participants = o.viewParticipants(event_id)
        assert isinstance(participants, list)

    def test_send_announcement(self, session):
        o = _create_organizer(session)
        assert o.sendAnnouncement(1, "Hello!") is True


# =============================================================================
# Admin
# =============================================================================

class TestAdmin:
    def test_create_admin(self, session):
        from werkzeug.security import generate_password_hash
        a = Admin(
            admin_name=Nickname("admin"),
            email=Email("admin@example.com"),
        )
        a.set_password("adminpass")
        session.add(a)
        session.commit()
        assert a.admin_id is not None

    def test_admin_review_event(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        a = Admin(admin_name=Nickname("super"), email=Email("super@test.com"))
        a.set_password("pw")
        session.add(a)
        session.commit()

        assert a.approveEvent(e.event_id) is True
        assert e.event_status == "Open"

        assert a.rejectEvent(e.event_id) is True
        assert e.event_status == "Cancelled"

    def test_admin_review_nonexistent_event(self, session):
        a = Admin(admin_name=Nickname("boss"), email=Email("boss@test.com"))
        a.set_password("pw")
        session.add(a)
        session.commit()
        assert a.reviewEvent(99999, EventStatus("Open")) is False

    def test_admin_manage_users(self, session):
        a = Admin(admin_name=Nickname("master"), email=Email("master@test.com"))
        a.set_password("pw")
        session.add(a)
        session.commit()
        assert a.manageUsers(1) is True

    def test_admin_generate_report(self, session):
        a = Admin(admin_name=Nickname("reporter"), email=Email("rep@test.com"))
        a.set_password("pw")
        session.add(a)
        session.commit()
        report = a.generateReport()
        assert "Total events" in report


# =============================================================================
# MusicEvent
# =============================================================================

class TestMusicEvent:
    def test_create_event(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        assert e.event_id is not None
        assert str(e.event_status) == "Open"

    def test_publish(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        e.event_status = EventStatus("draft")
        session.commit()
        assert e.publish() is True
        assert e.event_status == "Open"

    def test_cancel(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        assert e.cancel() is True
        assert e.event_status == "Cancelled"

    def test_update_info(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        result = e.updateInfo(
            EventTitle("Updated"),
            Text200("New description"),
            DateTime(datetime(2026, 12, 25)),
            DateTime(datetime(2026, 12, 25, 4)),
        )
        assert result is True
        assert str(e.event_title) == "Updated"

    def test_is_full(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = MusicEvent(
            event_title=EventTitle("Small Event"),
            description=Text200("Limited seats"),
            start_time=DateTime(datetime(2026, 8, 1)),
            end_time=DateTime(datetime(2026, 8, 1, 3)),
            capacity=Capacity(1),
            age_restriction=AgeRestriction(0),
            event_status=EventStatus("Open"),
            music_genre=MusicGenre("Jazz"),
            organizer_id=o.organizer_id,
            venue_id=v.venue_id,
        )
        session.add(e)
        session.commit()
        assert e.isFull() is False

    def test_event_venue_relationship(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        assert e.venue is not None
        assert str(e.venue.venue_name) == "Test Venue"

    def test_event_organizer_relationship(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        assert e.organizer is not None
        assert e.organizer.organizer_id == o.organizer_id


# =============================================================================
# Venue
# =============================================================================

class TestVenue:
    def test_create_venue(self, session):
        v = _create_venue(session)
        assert str(v.venue_name) == "Test Venue"
        assert int(v.capacity) == 500

    def test_check_availability_no_conflict(self, session):
        v = _create_venue(session)
        available = v.checkAvailability(
            datetime(2026, 12, 1, 10, 0),
            datetime(2026, 12, 1, 14, 0),
        )
        assert available is True

    def test_check_availability_with_conflict(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = MusicEvent(
            event_title=EventTitle("Blocked"),
            description=Text200("Blocks the venue"),
            start_time=DateTime(datetime(2026, 12, 1, 10, 0)),
            end_time=DateTime(datetime(2026, 12, 1, 14, 0)),
            capacity=Capacity(100),
            age_restriction=AgeRestriction(0),
            event_status=EventStatus("Open"),
            music_genre=MusicGenre("Rock"),
            organizer_id=o.organizer_id,
            venue_id=v.venue_id,
        )
        session.add(e)
        session.commit()

        available = v.checkAvailability(
            datetime(2026, 12, 1, 12, 0),
            datetime(2026, 12, 1, 16, 0),
        )
        assert available is False


# =============================================================================
# Artist
# =============================================================================

class TestArtist:
    def test_create_artist(self, session):
        a = Artist(
            first_name=Name("Jimmy"),
            second_name=Name("Page"),
            artist_type=ArtistType("Guitarist"),
            music_genre=MusicGenre("Rock"),
            bio=Text100("Legendary guitarist"),
        )
        session.add(a)
        session.commit()
        assert a.artist_id is not None

    def test_update_profile(self, session):
        a = Artist(
            first_name=Name("Old"),
            second_name=Name("Name"),
            artist_type=ArtistType("Solo"),
            music_genre=MusicGenre("Jazz"),
            bio=Text100("Bio"),
        )
        session.add(a)
        session.commit()
        result = a.updateProfile(Name("New"), Name("Name"), Text100("Updated bio"))
        assert result is True
        assert str(a.first_name) == "New"

    def test_view_events(self, session):
        a = Artist(
            first_name=Name("Taylor"),
            second_name=Name("Swift"),
            artist_type=ArtistType("Singer"),
            music_genre=MusicGenre("Concert"),
            bio=Text100("Famous singer"),
        )
        session.add(a)
        session.commit()
        events = a.viewEvents()
        assert isinstance(events, list)


# =============================================================================
# Registration
# =============================================================================

class TestRegistration:
    def test_create_registration(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)

        r = Registration(
            participant_id=p.participant_id,
            event_id=e.event_id,
        )
        session.add(r)
        session.commit()
        assert r.registration_id is not None
        assert r.registration_status == "Pending"

    def test_confirm_registration(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        r = Registration(participant_id=p.participant_id, event_id=e.event_id)
        session.add(r)
        session.commit()

        assert r.confirmRegistration() is True
        assert r.registration_status == "Confirmed"

    def test_cancel_registration(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        r = Registration(participant_id=p.participant_id, event_id=e.event_id)
        session.add(r)
        session.commit()

        assert r.cancelRegistration() is True
        assert r.registration_status == "Cancelled"

    def test_mark_checked_in(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        r = Registration(participant_id=p.participant_id, event_id=e.event_id)
        session.add(r)
        session.commit()

        assert r.markCheckedIn() is True
        assert r.check_in_status == "CheckedIn"


# =============================================================================
# Ticket
# =============================================================================

class TestTicket:
    def _make_ticket(self, session, ticket_type="standard", price="10.00"):
        """Helper: create a ticket with QR code generated before commit."""
        from app.domain.value_objects import QRCode
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        r = Registration(participant_id=p.participant_id, event_id=e.event_id)
        session.add(r)
        session.commit()

        import uuid
        t = Ticket(
            ticket_type=TicketType(ticket_type),
            price=Money(Decimal(price)),
            qr_code=QRCode(str(uuid.uuid4())),
            registration_id=r.registration_id,
        )
        session.add(t)
        session.commit()
        return t

    def test_create_ticket(self, session):
        t = self._make_ticket(session)
        assert t.ticket_id is not None

    def test_generate_qr_code(self, session):
        t = self._make_ticket(session, "vip", "99.99")
        old_code = str(t.qr_code)
        code = t.generateQRCode()
        assert len(code) > 0
        assert str(t.qr_code) != old_code

    def test_validate_ticket(self, session):
        t = self._make_ticket(session)
        from app.domain.value_objects import QRCode
        assert t.validateTicket(QRCode(str(t.qr_code))) is True

    def test_validate_ticket_wrong_code(self, session):
        t = self._make_ticket(session)
        from app.domain.value_objects import QRCode
        assert t.validateTicket(QRCode("wrong-code")) is False

    def test_cancel_ticket(self, session):
        t = self._make_ticket(session, "free", "0.00")
        assert t.cancelTicket() is True
        assert t.ticket_status == "Cancelled"


# =============================================================================
# Payment
# =============================================================================

class TestPayment:
    def _setup_payment(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)
        r = Registration(participant_id=p.participant_id, event_id=e.event_id)
        session.add(r)
        session.commit()
        return r

    def test_create_payment(self, session):
        r = self._setup_payment(session)
        now = datetime.now(timezone.utc)
        pmt = Payment(
            amount=Money(Decimal("29.99")),
            payment_method=PaymentMethod("card"),
            payment_time=DateTime(now),
            registration_id=r.registration_id,
        )
        session.add(pmt)
        session.commit()
        assert pmt.payment_id is not None
        assert pmt.payment_status == "Pending"

    def test_pay(self, session):
        r = self._setup_payment(session)
        now = datetime.now(timezone.utc)
        pmt = Payment(
            amount=Money(Decimal("0.00")),
            payment_method=PaymentMethod("free"),
            payment_time=DateTime(now),
            registration_id=r.registration_id,
        )
        session.add(pmt)
        session.commit()

        result = pmt.pay(Money(Decimal("29.99")), PaymentMethod("card"))
        assert result is True
        assert pmt.payment_status == "Paid"
        assert str(pmt.amount) == "29.99"

    def test_refund(self, session):
        r = self._setup_payment(session)
        now = datetime.now(timezone.utc)
        pmt = Payment(
            amount=Money(Decimal("50.00")),
            payment_method=PaymentMethod("paypal"),
            payment_time=DateTime(now),
            registration_id=r.registration_id,
        )
        session.add(pmt)
        session.commit()

        assert pmt.refund(Money(Decimal("50.00"))) is True
        assert pmt.payment_status == "Refunded"

    def test_verify_payment(self, session):
        r = self._setup_payment(session)
        now = datetime.now(timezone.utc)
        pmt = Payment(
            amount=Money(Decimal("10.00")),
            payment_method=PaymentMethod("card"),
            payment_time=DateTime(now),
            registration_id=r.registration_id,
        )
        session.add(pmt)
        session.commit()
        pmt.pay(Money(Decimal("10.00")), PaymentMethod("card"))

        assert pmt.verifyPayment(pmt.payment_id) is True


# =============================================================================
# Comment
# =============================================================================

class TestComment:
    def test_create_comment(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)

        c = Comment(
            content=Text500("Great event!"),
            user_id=p.user_id,
            event_id=e.event_id,
        )
        session.add(c)
        session.commit()
        assert c.comment_id is not None
        assert str(c.content) == "Great event!"

    def test_comment_user_relationship(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)

        c = Comment(
            content=Text500("Nice"),
            user_id=p.user_id,
            event_id=e.event_id,
        )
        session.add(c)
        session.commit()
        assert c.user is not None
        assert c.user.user_id == p.user_id

    def test_comment_event_relationship(self, session):
        p = _create_participant(session)
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)

        c = Comment(
            content=Text500("Cool!"),
            user_id=p.user_id,
            event_id=e.event_id,
        )
        session.add(c)
        session.commit()
        assert c.music_event is not None
        assert c.music_event.event_id == e.event_id


# =============================================================================
# Announcement
# =============================================================================

class TestAnnouncement:
    def test_create_announcement(self, session):
        v = _create_venue(session)
        o = _create_organizer(session)
        e = _create_event(session, o, v)

        a = Announcement(
            content=Text500("Event starts at 7pm!"),
            event_id=e.event_id,
        )
        session.add(a)
        session.commit()
        assert a.announcement_id is not None
