"""Tests for WTForms form classes and validation."""

from decimal import Decimal

import pytest
from flask import Flask

from app.forms.auth_forms import LoginForm, SignupForm
from app.forms.event_forms import EventForm
from app.forms.payment_forms import PaymentForm
from app.forms.comment_forms import CommentForm


def _form_context(form_class, **data):
    """Create a Flask app context and instantiate a form with CSRF disabled."""
    app = Flask(__name__)
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_request_context():
        form = form_class(data=data)
        # Set choices for SelectFields if they exist
        if hasattr(form, "venue_id"):
            form.venue_id.choices = [(1, "Test Venue")]
        if hasattr(form, "music_genre") and not form.music_genre.choices:
            form.music_genre.choices = [
                ("Jazz", "Jazz"), ("Rock", "Rock"),
                ("Campus Festival", "Campus Festival"),
                ("Acoustic", "Acoustic"), ("Concert", "Concert"),
            ]
        if hasattr(form, "payment_method") and not form.payment_method.choices:
            form.payment_method.choices = [
                ("card", "Card"), ("paypal", "PayPal"),
                ("bank_transfer", "Bank Transfer"), ("free", "Free"),
            ]
    return form


# =============================================================================
# LoginForm
# =============================================================================

class TestLoginForm:
    def test_valid(self):
        form = _form_context(LoginForm, email="test@example.com", password="secret")
        assert form.validate() is True

    def test_email_required(self):
        form = _form_context(LoginForm, email="", password="secret")
        assert form.validate() is False
        assert "email" in form.errors

    def test_email_invalid_format(self):
        form = _form_context(LoginForm, email="notanemail", password="secret")
        assert form.validate() is False

    def test_password_required(self):
        form = _form_context(LoginForm, email="test@example.com", password="")
        assert form.validate() is False
        assert "password" in form.errors


# =============================================================================
# SignupForm
# =============================================================================

class TestSignupForm:
    def test_valid(self):
        form = _form_context(SignupForm,
            nickname="johndoe",
            email="john@example.com",
            password="secure123",
            first_name="John",
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is True

    def test_nickname_required(self):
        form = _form_context(SignupForm,
            nickname="",
            email="john@example.com",
            password="secure123",
            first_name="John",
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is False
        assert "nickname" in form.errors

    def test_nickname_max_length(self):
        form = _form_context(SignupForm,
            nickname="a" * 51,
            email="john@example.com",
            password="secure123",
            first_name="John",
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is False

    def test_nickname_boundary_50(self):
        form = _form_context(SignupForm,
            nickname="a" * 50,
            email="john@example.com",
            password="secure123",
            first_name="John",
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is True

    def test_email_required(self):
        form = _form_context(SignupForm,
            nickname="johndoe",
            email="",
            password="secure123",
            first_name="John",
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is False

    def test_password_required(self):
        form = _form_context(SignupForm,
            nickname="johndoe",
            email="john@example.com",
            password="",
            first_name="John",
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is False

    def test_first_name_boundary(self):
        form = _form_context(SignupForm,
            nickname="johndoe",
            email="john@example.com",
            password="pw",
            first_name="A" * 81,
            second_name="Doe",
            contact_number="0412345678",
            street_address="123 Main St",
        )
        assert form.validate() is False

    def test_contact_number_boundary(self):
        form = _form_context(SignupForm,
            nickname="johndoe",
            email="john@example.com",
            password="pw",
            first_name="John",
            second_name="Doe",
            contact_number="1" * 21,
            street_address="123 Main St",
        )
        assert form.validate() is False

    def test_street_address_boundary(self):
        form = _form_context(SignupForm,
            nickname="johndoe",
            email="john@example.com",
            password="pw",
            first_name="John",
            second_name="Doe",
            contact_number="0400000000",
            street_address="A" * 256,
        )
        assert form.validate() is False


# =============================================================================
# EventForm
# =============================================================================

class TestEventForm:
    def test_valid(self):
        form = _form_context(EventForm,
            event_title="Rock Concert",
            description="A great rock concert",
            music_genre="Rock",
            start_time="2026-08-01T19:00",
            end_time="2026-08-01T22:00",
            capacity=100,
            ticket_price=Decimal("25.00"),
            age_restriction=18,
            venue_id=1,
        )
        assert form.validate() is True

    def test_event_title_required(self):
        form = _form_context(EventForm,
            event_title="",
            description="A great rock concert",
            music_genre="Rock",
            start_time="2026-08-01T19:00",
            end_time="2026-08-01T22:00",
            capacity=100,
            ticket_price=Decimal("25.00"),
            age_restriction=18,
            venue_id=1,
        )
        assert form.validate() is False
        assert "event_title" in form.errors

    def test_event_title_max_length(self):
        form = _form_context(EventForm,
            event_title="A" * 101,
            description="A great rock concert",
            music_genre="Rock",
            start_time="2026-08-01T19:00",
            end_time="2026-08-01T22:00",
            capacity=100,
            ticket_price=Decimal("25.00"),
            age_restriction=18,
            venue_id=1,
        )
        assert form.validate() is False

    def test_description_max_length(self):
        form = _form_context(EventForm,
            event_title="Rock Concert",
            description="A" * 201,
            music_genre="Rock",
            start_time="2026-08-01T19:00",
            end_time="2026-08-01T22:00",
            capacity=100,
            ticket_price=Decimal("25.00"),
            age_restriction=18,
            venue_id=1,
        )
        assert form.validate() is False

    def test_capacity_minimum(self):
        form = _form_context(EventForm,
            event_title="Rock Concert",
            description="A great rock concert",
            music_genre="Rock",
            start_time="2026-08-01T19:00",
            end_time="2026-08-01T22:00",
            capacity=0,
            ticket_price=Decimal("25.00"),
            age_restriction=18,
            venue_id=1,
        )
        assert form.validate() is False

    def test_age_restriction_boundary(self):
        # age_restriction=1 is valid (0 is falsy, caught by DataRequired)
        form = _form_context(EventForm)
        form.event_title.data = "Rock Concert"
        form.description.data = "A great rock concert"
        form.music_genre.data = "Rock"
        form.start_time.data = "2026-08-01T19:00"
        form.end_time.data = "2026-08-01T22:00"
        form.capacity.data = 100
        form.ticket_price.data = Decimal("25.00")
        form.age_restriction.data = 1
        form.venue_id.data = 1
        assert form.validate() is True

        # age_restriction=101 is invalid (exceeds max=100)
        form2 = _form_context(EventForm)
        form2.event_title.data = "Rock Concert"
        form2.description.data = "A great rock concert"
        form2.music_genre.data = "Rock"
        form2.start_time.data = "2026-08-01T19:00"
        form2.end_time.data = "2026-08-01T22:00"
        form2.capacity.data = 100
        form2.ticket_price.data = Decimal("25.00")
        form2.age_restriction.data = 101
        form2.venue_id.data = 1
        assert form2.validate() is False

    def test_description_required(self):
        form = _form_context(EventForm,
            event_title="Rock Concert",
            description="",
            music_genre="Rock",
            start_time="2026-08-01T19:00",
            end_time="2026-08-01T22:00",
            capacity=100,
            ticket_price=Decimal("25.00"),
            age_restriction=18,
            venue_id=1,
        )
        assert form.validate() is False


# =============================================================================
# PaymentForm
# =============================================================================

class TestPaymentForm:
    def test_valid(self):
        from decimal import Decimal
        form = _form_context(PaymentForm)
        form.amount.data = Decimal("29.99")
        form.payment_method.data = "card"
        assert form.validate() is True

    def test_amount_required(self):
        form = _form_context(PaymentForm, payment_method="card")
        # Empty amount should fail NumberRange
        assert form.validate() is False

    def test_amount_negative(self):
        from decimal import Decimal
        form = _form_context(PaymentForm)
        form.amount.data = Decimal("-1.00")
        form.payment_method.data = "card"
        assert form.validate() is False

    def test_amount_valid(self):
        from decimal import Decimal
        form = _form_context(PaymentForm)
        form.amount.data = Decimal("0.01")
        form.payment_method.data = "free"
        assert form.validate() is True

    def test_payment_method_required(self):
        from decimal import Decimal
        form = _form_context(PaymentForm)
        form.amount.data = Decimal("10.00")
        form.payment_method.data = ""
        assert form.validate() is False

    def test_invalid_payment_method(self):
        from decimal import Decimal
        form = _form_context(PaymentForm)
        form.amount.data = Decimal("10.00")
        form.payment_method.data = "bitcoin"
        assert form.validate() is False


# =============================================================================
# CommentForm
# =============================================================================

class TestCommentForm:
    def test_valid(self):
        form = _form_context(CommentForm, content="Great event!")
        assert form.validate() is True

    def test_content_required(self):
        form = _form_context(CommentForm, content="")
        assert form.validate() is False

    def test_content_max_length(self):
        form = _form_context(CommentForm, content="A" * 501)
        assert form.validate() is False

    def test_content_boundary_500(self):
        form = _form_context(CommentForm, content="A" * 500)
        assert form.validate() is True

    def test_content_boundary_1(self):
        form = _form_context(CommentForm, content="A")
        assert form.validate() is True
