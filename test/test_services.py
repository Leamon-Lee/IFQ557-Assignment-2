"""Tests for service layer classes."""

from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest

from app.domain.value_objects import (
    Address, AgeRestriction, Capacity, CheckInStatus, ContactNumber,
    DateTime, Email, EventStatus, EventTitle, Money, MusicGenre, Name,
    Nickname, PasswordHash, PaymentMethod, RegistrationStatus, Text200,
    TicketType, Text500
)
from app.extensions import db
from app.models.user import User
from app.models.participant import Participant
from app.models.organizer import Organizer
from app.models.music_event import MusicEvent
from app.models.venue import Venue
from app.models.registration import Registration
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.services.auth_service import AuthService
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService
from app.services.payment_service import PaymentService
from app.services.comment_service import CommentService


def _make_organizer(session):
    from werkzeug.security import generate_password_hash
    from app.domain.value_objects import OrganizationName
    pw = generate_password_hash("orgpass")
    o = Organizer(
        nickname=Nickname("org1"),
        email=Email("org1@svc.test"),
        password_hash=PasswordHash(pw),
        contact_number=ContactNumber("0411111111"),
        street_address=Address("123 Org St"),
        first_name=Name("Jane"),
        second_name=Name("Org"),
    )
    o.organization_name = OrganizationName("OrgCo")
    session.add(o)
    session.commit()
    return o


def _make_venue(session):
    from app.domain.value_objects import VenueName, City, Room
    v = Venue(
        venue_name=VenueName("Svc Venue"),
        address=Address("456 St"),
        city=City("Sydney"),
        room=Room("A"),
        capacity=Capacity(300),
    )
    session.add(v)
    session.commit()
    return v


def _make_event(session, org, venue):
    now = datetime.now(timezone.utc)
    e = MusicEvent(
        event_title=EventTitle("Service Test"),
        description=Text200("For service tests"),
        start_time=DateTime(now + timedelta(days=14)),
        end_time=DateTime(now + timedelta(days=14, hours=2)),
        capacity=Capacity(200),
        age_restriction=AgeRestriction(0),
        event_status=EventStatus("Open"),
        music_genre=MusicGenre("Rock"),
        organizer_id=org.organizer_id,
        venue_id=venue.venue_id,
    )
    session.add(e)
    session.commit()
    return e


def _make_participant(session):
    from werkzeug.security import generate_password_hash
    pw = generate_password_hash("userpass")
    p = Participant(
        nickname=Nickname("svcuser"),
        email=Email("svcuser@svc.test"),
        password_hash=PasswordHash(pw),
        contact_number=ContactNumber("0400000000"),
        street_address=Address("1 User Rd"),
        first_name=Name("Bob"),
        second_name=Name("User"),
    )
    session.add(p)
    session.commit()
    return p


# =============================================================================
# AuthService
# =============================================================================

class TestAuthService:
    def test_signup_success(self, session):
        svc = AuthService()
        ok, user, msg = svc.signup(
            nickname="newuser",
            email="newuser@test.com",
            password="secure123",
            first_name="Alice",
            second_name="Smith",
            contact_number="0411111111",
            street_address="1 Main St",
        )
        assert ok is True
        assert user is not None
        assert "successful" in msg.lower()
        assert isinstance(user, Participant)

    def test_signup_duplicate_email(self, session):
        svc = AuthService()
        svc.signup("u1", "dup@test.com", "pw", "A", "B", "0400000000", "1 St")
        ok, user, msg = svc.signup("u2", "dup@test.com", "pw", "C", "D", "0400000001", "2 St")
        assert ok is False
        assert user is None
        assert "already registered" in msg.lower()

    def test_login_success(self, app, session):
        svc = AuthService()
        svc.signup("logme", "logme@test.com", "mypassword", "X", "Y", "0400000002", "3 St")
        with app.test_request_context():
            ok, user, msg = svc.login("logme@test.com", "mypassword")
        assert ok is True
        assert msg == "Login successful."

    def test_login_wrong_password(self, session):
        svc = AuthService()
        svc.signup("badpw", "badpw@test.com", "correct", "X", "Y", "0400000003", "4 St")
        ok, user, msg = svc.login("badpw@test.com", "wrong")
        assert ok is False
        assert "password" in msg.lower()

    def test_login_nonexistent_email(self, session):
        svc = AuthService()
        ok, user, msg = svc.login("nobody@test.com", "password")
        assert ok is False
        assert "no account" in msg.lower()

    def test_logout(self, app, session):
        svc = AuthService()
        with app.test_request_context():
            assert svc.logout() is True

    def test_signup_invalid_email_raises(self, session):
        svc = AuthService()
        with pytest.raises(ValueError):
            svc.signup("user", "not-an-email", "pw", "A", "B", "0400000000", "1 St")

    def test_signup_invalid_nickname_raises(self, session):
        svc = AuthService()
        with pytest.raises(ValueError):
            svc.signup("", "ok@test.com", "pw", "A", "B", "0400000000", "1 St")


# =============================================================================
# EventService
# =============================================================================

class TestEventService:
    def test_list_events_all(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        _make_event(session, o, v)
        _make_event(session, o, v)

        svc = EventService()
        events = svc.listEvents()
        assert len(events) >= 2

    def test_list_events_by_genre(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e1 = _make_event(session, o, v)
        now = datetime.now(timezone.utc)
        e2 = MusicEvent(
            event_title=EventTitle("Jazz Night"),
            description=Text200("Jazz event"),
            start_time=DateTime(now + timedelta(days=30)),
            end_time=DateTime(now + timedelta(days=30, hours=3)),
            capacity=Capacity(100),
            age_restriction=AgeRestriction(0),
            event_status=EventStatus("Open"),
            music_genre=MusicGenre("Jazz"),
            organizer_id=o.organizer_id,
            venue_id=v.venue_id,
        )
        session.add(e2)
        session.commit()

        svc = EventService()
        jazz_events = svc.listEvents(genre="Jazz")
        for e in jazz_events:
            assert str(e.music_genre) == "Jazz"

    def test_list_events_by_search(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        _make_event(session, o, v)

        svc = EventService()
        results = svc.listEvents(search="Service")
        assert len(results) >= 1

    def test_get_event(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)

        svc = EventService()
        found = svc.getEvent(e.event_id)
        assert found is not None
        assert found.event_id == e.event_id

    def test_get_event_not_found(self, session):
        svc = EventService()
        assert svc.getEvent(99999) is None

    def test_get_confirmed_count(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)
        r = Registration(participant_id=p.participant_id, event_id=e.event_id)
        session.add(r)
        session.commit()
        r.confirmRegistration()

        svc = EventService()
        assert svc.getConfirmedCount(e.event_id) == 1

    def test_get_remaining_tickets(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)  # capacity=200

        svc = EventService()
        assert svc.getRemainingTickets(e.event_id) == 200

    def test_get_remaining_tickets_event_not_found(self, session):
        svc = EventService()
        assert svc.getRemainingTickets(99999) == 0


# =============================================================================
# RegistrationService
# =============================================================================

class TestRegistrationService:
    def test_register_event(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = RegistrationService()
        reg_id = svc.registerEvent(p.participant_id, e.event_id)
        assert reg_id > 0

        reg = db.session.get(Registration, reg_id)
        assert reg.registration_status == "Confirmed"
        assert reg.ticket is not None
        assert reg.payment is not None
        assert reg.payment.payment_status == "Paid"

    def test_register_event_free(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = RegistrationService()
        reg_id = svc.registerEvent(
            p.participant_id, e.event_id,
            ticket_type="free", price=Decimal("0.00"), payment_method="free"
        )
        assert reg_id > 0

    def test_cancel_registration(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = RegistrationService()
        reg_id = svc.registerEvent(p.participant_id, e.event_id)

        assert svc.cancelRegistration(reg_id) is True
        reg = db.session.get(Registration, reg_id)
        assert reg.registration_status == "Cancelled"

    def test_cancel_nonexistent(self, session):
        svc = RegistrationService()
        assert svc.cancelRegistration(99999) is False

    def test_mark_checked_in(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = RegistrationService()
        reg_id = svc.registerEvent(p.participant_id, e.event_id)

        assert svc.markCheckedIn(reg_id) is True
        reg = db.session.get(Registration, reg_id)
        assert reg.check_in_status == "CheckedIn"

    def test_get_registrations_by_participant(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = RegistrationService()
        svc.registerEvent(p.participant_id, e.event_id)

        regs = svc.getRegistrationsByParticipant(p.participant_id)
        assert len(regs) >= 1


# =============================================================================
# PaymentService
# =============================================================================

class TestPaymentService:
    def test_pay(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        reg_svc = RegistrationService()
        reg_id = reg_svc.registerEvent(p.participant_id, e.event_id)

        # Payment already created via registration service; test update
        svc = PaymentService()
        payment = Payment.query.filter_by(registration_id=reg_id).first()
        assert svc.pay(reg_id, Decimal("19.99"), "card") is True
        assert payment.payment_status == "Paid"

    def test_pay_nonexistent_registration(self, session):
        svc = PaymentService()
        assert svc.pay(99999, Decimal("10.00"), "card") is False

    def test_refund(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        reg_svc = RegistrationService()
        reg_id = reg_svc.registerEvent(p.participant_id, e.event_id)
        payment = Payment.query.filter_by(registration_id=reg_id).first()

        svc = PaymentService()
        assert svc.refund(payment.payment_id) is True

    def test_verify_payment(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        reg_svc = RegistrationService()
        reg_id = reg_svc.registerEvent(p.participant_id, e.event_id)
        payment = Payment.query.filter_by(registration_id=reg_id).first()

        svc = PaymentService()
        assert svc.verifyPayment(payment.payment_id) is True


# =============================================================================
# CommentService
# =============================================================================

class TestCommentService:
    def test_add_comment(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = CommentService()
        comment = svc.addComment(p.user_id, e.event_id, "Excellent event!")
        assert comment.comment_id is not None
        assert str(comment.content) == "Excellent event!"

    def test_get_comments_by_event(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = CommentService()
        svc.addComment(p.user_id, e.event_id, "First")
        svc.addComment(p.user_id, e.event_id, "Second")

        comments = svc.getCommentsByEvent(e.event_id)
        assert len(comments) == 2
        # Most recent first
        assert str(comments[0].content) == "Second"

    def test_add_comment_invalid_content(self, session):
        o = _make_organizer(session)
        v = _make_venue(session)
        e = _make_event(session, o, v)
        p = _make_participant(session)

        svc = CommentService()
        with pytest.raises(ValueError):
            svc.addComment(p.user_id, e.event_id, "")
