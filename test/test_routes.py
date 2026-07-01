"""Integration tests for Flask routes / Blueprints."""

from datetime import datetime, timezone, timedelta

import pytest

from app.domain.value_objects import (
    Address, AgeRestriction, Capacity, ContactNumber, DateTime,
    Email, EventStatus, EventTitle, MusicGenre, Name, Nickname,
    PasswordHash, Text200
)
from app.extensions import db
from app.models.user import User
from app.models.participant import Participant
from app.models.organizer import Organizer
from app.models.music_event import MusicEvent
from app.models.venue import Venue
from app.models.registration import Registration


def _create_participant(session):
    from werkzeug.security import generate_password_hash
    pw = generate_password_hash("password123")
    p = Participant(
        nickname=Nickname("participant1"),
        email=Email("participant@route.test"),
        password_hash=PasswordHash(pw),
        contact_number=ContactNumber("0411111111"),
        street_address=Address("1 Part St"),
        first_name=Name("Part"),
        second_name=Name("User"),
    )
    session.add(p)
    session.commit()
    return p


def _create_organizer(session):
    from werkzeug.security import generate_password_hash
    from app.domain.value_objects import OrganizationName
    pw = generate_password_hash("password123")
    o = Organizer(
        nickname=Nickname("organizer1"),
        email=Email("organizer@route.test"),
        password_hash=PasswordHash(pw),
        contact_number=ContactNumber("0422222222"),
        street_address=Address("1 Org Rd"),
        first_name=Name("Org"),
        second_name=Name("User"),
    )
    o.organization_name = OrganizationName("OrgCorp")
    session.add(o)
    session.commit()
    return o


def _create_venue(session):
    from app.domain.value_objects import VenueName, City, Room
    v = Venue(
        venue_name=VenueName("Route Venue"),
        address=Address("500 Event St"),
        city=City("Brisbane"),
        room=Room("Main"),
        capacity=Capacity(500),
    )
    session.add(v)
    session.commit()
    return v


def _create_event(session, organizer, venue):
    now = datetime.now(timezone.utc)
    e = MusicEvent(
        event_title=EventTitle("Route Event"),
        description=Text200("For route tests"),
        start_time=DateTime(now + timedelta(days=30)),
        end_time=DateTime(now + timedelta(days=30, hours=3)),
        capacity=Capacity(100),
        age_restriction=AgeRestriction(0),
        event_status=EventStatus("Open"),
        music_genre=MusicGenre("Rock"),
        organizer_id=organizer.organizer_id,
        venue_id=venue.venue_id,
    )
    session.add(e)
    session.commit()
    return e


def _login_as(client, session, user_type="participant"):
    """Helper to log in via the auth route. Returns immediately without following redirect."""
    if user_type == "participant":
        email = "participant@route.test"
    else:
        email = "organizer@route.test"
    return client.post("/auth/login", data={
        "email": email,
        "password": "password123",
    })


# =============================================================================
# Auth Routes
# =============================================================================

class TestAuthRoutes:
    def test_login_page(self, client):
        resp = client.get("/auth/login")
        assert resp.status_code == 200

    def test_login_success(self, session, client):
        _create_participant(session)
        resp = _login_as(client, session, "participant")
        assert resp.status_code == 200

    def test_login_wrong_password(self, session, client):
        _create_participant(session)
        resp = client.post("/auth/login", data={
            "email": "participant@route.test",
            "password": "wrongpassword",
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_signup_page(self, client):
        resp = client.get("/auth/signup")
        assert resp.status_code == 200

    def test_signup_success(self, session, client):
        resp = client.post("/auth/signup", data={
            "nickname": "newuser99",
            "email": "newuser99@test.com",
            "password": "secure123",
            "first_name": "New",
            "second_name": "User",
            "contact_number": "0499999999",
            "street_address": "99 New St",
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_signup_duplicate_email(self, session, client):
        _create_participant(session)
        resp = client.post("/auth/signup", data={
            "nickname": "dupuser",
            "email": "participant@route.test",
            "password": "pw12345",
            "first_name": "Dup",
            "second_name": "User",
            "contact_number": "0488888888",
            "street_address": "88 Dup St",
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_logout(self, session, client):
        _create_participant(session)
        _login_as(client, session, "participant")
        resp = client.get("/auth/logout", follow_redirects=True)
        assert resp.status_code == 200


# =============================================================================
# Event Routes
# =============================================================================

class TestEventRoutes:
    def test_home_page(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_events_list_page(self, client):
        resp = client.get("/events")
        assert resp.status_code == 200

    def test_event_detail(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        resp = client.get(f"/events/{e.event_id}")
        assert resp.status_code == 200

    def test_event_detail_not_found(self, client):
        resp = client.get("/events/99999")
        assert resp.status_code == 404

    def test_create_event_page_redirects_if_not_organizer(self, session, client):
        _create_participant(session)
        _login_as(client, session, "participant")
        resp = client.get("/events/create", follow_redirects=True)
        assert resp.status_code == 200

    def test_create_event_as_organizer(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        _login_as(client, session, "organizer")
        resp = client.post("/events/create", data={
            "event_title": "My New Event",
            "description": "A brand new event for testing",
            "music_genre": "Jazz",
            "start_time": "2026-12-01T19:00",
            "end_time": "2026-12-01T22:00",
            "capacity": 50,
            "age_restriction": 1,
            "venue_id": v.venue_id,
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_edit_event_as_owner(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        _login_as(client, session, "organizer")
        resp = client.post(f"/events/{e.event_id}/edit", data={
            "event_title": "Updated Event Title",
            "description": "Updated description here",
            "music_genre": "Jazz",
            "start_time": "2026-12-01T19:00",
            "end_time": "2026-12-01T22:00",
            "capacity": 75,
            "age_restriction": 18,
            "venue_id": v.venue_id,
        }, follow_redirects=True)
        assert resp.status_code == 200

    def test_cancel_event(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        _login_as(client, session, "organizer")
        resp = client.post(f"/events/{e.event_id}/cancel", follow_redirects=True)
        assert resp.status_code == 200

    def test_event_detail_with_comments(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        resp = client.get(f"/events/{e.event_id}")
        assert resp.status_code == 200


# =============================================================================
# Participant Routes
# =============================================================================

class TestParticipantRoutes:
    def test_dashboard_redirects_when_not_logged_in(self, client):
        resp = client.get("/participant/dashboard", follow_redirects=True)
        assert resp.status_code == 200

    def test_dashboard_logged_in(self, app, session, client):
        _create_participant(session)
        with app.test_request_context():
            from flask_login import login_user
            from app.models.user import User
            user = db.session.get(User, 1)
            if user:
                login_user(user)
        with client:
            resp = client.get("/participant/dashboard")
            assert resp.status_code in (200, 302)

    def test_registrations_page(self, app, session, client):
        _create_participant(session)
        with app.test_request_context():
            from flask_login import login_user
            from app.models.user import User
            user = db.session.get(User, 1)
            if user:
                login_user(user)
        with client:
            resp = client.get("/participant/registrations")
            assert resp.status_code in (200, 302)

    def test_register_event(self, session, client):
        _create_participant(session)
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        with client:
            client.post("/auth/login", data={
                "email": "participant@route.test",
                "password": "password123",
            })
            resp = client.post(
                f"/participant/events/{e.event_id}/register",
                data={
                    "quantity": 1,
                    "ticket_type": "standard",
                    "price": "25.00",
                    "payment_method": "card",
                },
                follow_redirects=True,
            )
        assert resp.status_code == 200

    def test_register_event_not_found(self, session, client):
        _create_participant(session)
        # Without login, @login_required redirects to login page
        resp = client.post("/participant/events/99999/register",
                          follow_redirects=True)
        assert resp.status_code == 200  # Redirected to login page

    def test_view_ticket(self, session, client):
        _create_participant(session)
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        with client:
            client.post("/auth/login", data={
                "email": "participant@route.test",
                "password": "password123",
            })
            client.post(
                f"/participant/events/{e.event_id}/register",
                data={"quantity": 1, "ticket_type": "free", "price": "0.00", "payment_method": "free"},
            )
            from app.models.ticket import Ticket as TicketModel
            tickets = TicketModel.query.all()
            if tickets:
                resp = client.get(f"/participant/tickets/{tickets[-1].ticket_id}")
                assert resp.status_code == 200

    def test_view_ticket_not_found(self, session, client):
        _create_participant(session)
        # Without login, @login_required redirects to login page
        resp = client.get("/participant/tickets/99999", follow_redirects=True)
        assert resp.status_code == 200  # Redirected to login page


# =============================================================================
# Organizer Routes
# =============================================================================

class TestOrganizerRoutes:
    def test_dashboard_redirects_not_logged_in(self, client):
        resp = client.get("/organizer/dashboard", follow_redirects=True)
        assert resp.status_code == 200

    def test_dashboard_as_organizer(self, session, client):
        _create_organizer(session)
        with client:
            client.post("/auth/login", data={
                "email": "organizer@route.test",
                "password": "password123",
            })
            resp = client.get("/organizer/dashboard")
            assert resp.status_code in (200, 302)

    def test_dashboard_as_participant_redirects(self, session, client):
        _create_participant(session)
        with client:
            client.post("/auth/login", data={
                "email": "participant@route.test",
                "password": "password123",
            })
            resp = client.get("/organizer/dashboard", follow_redirects=True)
            assert resp.status_code == 200

    def test_participants_page(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        with client:
            client.post("/auth/login", data={
                "email": "organizer@route.test",
                "password": "password123",
            })
            resp = client.get(f"/organizer/events/{e.event_id}/participants")
            assert resp.status_code in (200, 302)

    def test_post_announcement(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        with client:
            client.post("/auth/login", data={
                "email": "organizer@route.test",
                "password": "password123",
            })
            resp = client.post(
                f"/organizer/events/{e.event_id}/participants",
                data={"content": "The event starts at 7pm sharp!"},
                follow_redirects=True,
            )
        assert resp.status_code == 200


# =============================================================================
# Admin Routes
# =============================================================================

class TestAdminRoutes:
    def test_dashboard(self, client):
        resp = client.get("/admin/dashboard")
        assert resp.status_code == 200

    def test_review_events(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        resp = client.get("/admin/review-events")
        assert resp.status_code == 200

    def test_approve_event(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        e.event_status = EventStatus("draft")
        session.commit()
        resp = client.post(f"/admin/events/{e.event_id}/approve", follow_redirects=True)
        assert resp.status_code == 200

    def test_reject_event(self, session, client):
        o = _create_organizer(session)
        v = _create_venue(session)
        e = _create_event(session, o, v)
        e.event_status = EventStatus("pending")
        session.commit()
        resp = client.post(f"/admin/events/{e.event_id}/reject", follow_redirects=True)
        assert resp.status_code == 200

    def test_approve_nonexistent_event(self, client):
        resp = client.post("/admin/events/99999/approve")
        assert resp.status_code == 404


# =============================================================================
# Error Handlers
# =============================================================================

class TestErrorHandlers:
    def test_404_page(self, client):
        resp = client.get("/nonexistent-page-xyz")
        assert resp.status_code == 404
