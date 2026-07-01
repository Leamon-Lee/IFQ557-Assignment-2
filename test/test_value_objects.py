"""Tests for all domain value objects with boundary testing."""

from datetime import datetime
from decimal import Decimal

import pytest

from app.domain.value_objects.address import Address
from app.domain.value_objects.age import Age
from app.domain.value_objects.age_restriction import AgeRestriction
from app.domain.value_objects.artist_type import ArtistType
from app.domain.value_objects.capacity import Capacity
from app.domain.value_objects.check_in_status import CheckInStatus
from app.domain.value_objects.city import City
from app.domain.value_objects.contact_number import ContactNumber
from app.domain.value_objects.date_time import DateTime
from app.domain.value_objects.email import Email
from app.domain.value_objects.event_status import EventStatus
from app.domain.value_objects.event_title import EventTitle
from app.domain.value_objects.money import Money
from app.domain.value_objects.music_genre import MusicGenre
from app.domain.value_objects.name import Name
from app.domain.value_objects.nickname import Nickname
from app.domain.value_objects.organization_name import OrganizationName
from app.domain.value_objects.password_hash import PasswordHash
from app.domain.value_objects.payment_method import PaymentMethod
from app.domain.value_objects.payment_status import PaymentStatus
from app.domain.value_objects.qr_code import QRCode
from app.domain.value_objects.registration_status import RegistrationStatus
from app.domain.value_objects.room import Room
from app.domain.value_objects.text100 import Text100
from app.domain.value_objects.text200 import Text200
from app.domain.value_objects.text500 import Text500
from app.domain.value_objects.ticket_status import TicketStatus
from app.domain.value_objects.ticket_type import TicketType
from app.domain.value_objects.venue_name import VenueName

# ID value objects
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.admin_id import AdminId
from app.domain.value_objects.artist_id import ArtistId
from app.domain.value_objects.event_id import EventId
from app.domain.value_objects.organizer_id import OrganizerId
from app.domain.value_objects.participant_id import ParticipantId
from app.domain.value_objects.payment_id import PaymentId
from app.domain.value_objects.registration_id import RegistrationId
from app.domain.value_objects.ticket_id import TicketId
from app.domain.value_objects.venue_id import VenueId


# =============================================================================
# Address
# =============================================================================

class TestAddress:
    def test_valid_address(self):
        a = Address("123 Main Street")
        assert str(a) == "123 Main Street"

    def test_min_length_boundary(self):
        Address("A")
        with pytest.raises(ValueError, match="must be 1 to 255"):
            Address("")

    def test_max_length_boundary(self):
        Address("A" * 255)
        with pytest.raises(ValueError, match="must be 1 to 255"):
            Address("A" * 256)

    def test_leading_trailing_spaces(self):
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            Address(" 123 Main St")
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            Address("123 Main St ")

    def test_frozen_immutable(self):
        a = Address("123 Main St")
        with pytest.raises(Exception):
            a.value = "changed"

    def test_equality(self):
        assert Address("X") == Address("X")
        assert Address("A") != Address("B")


# =============================================================================
# Age
# =============================================================================

class TestAge:
    def test_valid_age(self):
        assert int(Age(25)) == 25

    def test_lower_boundary(self):
        Age(0)
        with pytest.raises(ValueError, match="between 0 and 100"):
            Age(-1)

    def test_upper_boundary(self):
        Age(100)
        with pytest.raises(ValueError, match="between 0 and 100"):
            Age(101)

    def test_type_error_non_int(self):
        with pytest.raises(TypeError):
            Age("25")  # type: ignore
        with pytest.raises(TypeError):
            Age(25.5)  # type: ignore


# =============================================================================
# AgeRestriction
# =============================================================================

class TestAgeRestriction:
    def test_valid_values(self):
        assert int(AgeRestriction(0)) == 0
        assert int(AgeRestriction(18)) == 18
        assert int(AgeRestriction(100)) == 100

    def test_invalid_negative(self):
        with pytest.raises(ValueError):
            AgeRestriction(-1)

    def test_invalid_too_high(self):
        with pytest.raises(ValueError):
            AgeRestriction(101)


# =============================================================================
# ArtistType
# =============================================================================

class TestArtistType:
    def test_valid(self):
        assert str(ArtistType("Solo")) == "Solo"

    def test_min_length(self):
        ArtistType("X")
        with pytest.raises(ValueError, match="1 to 80"):
            ArtistType("")

    def test_max_length(self):
        ArtistType("A" * 80)
        with pytest.raises(ValueError, match="1 to 80"):
            ArtistType("A" * 81)

    def test_invalid_characters(self):
        with pytest.raises(ValueError, match="English letters"):
            ArtistType("123")


# =============================================================================
# Capacity
# =============================================================================

class TestCapacity:
    def test_valid_capacity(self):
        c = Capacity(100)
        assert int(c) == 100

    def test_zero_boundary(self):
        with pytest.raises(ValueError, match="greater than 0"):
            Capacity(0)

    def test_negative(self):
        with pytest.raises(ValueError, match="greater than 0"):
            Capacity(-1)

    def test_upper_boundary(self):
        Capacity(100000)
        with pytest.raises(ValueError, match="greater than 100000"):
            Capacity(100001)

    def test_type_error(self):
        with pytest.raises(TypeError):
            Capacity("100")  # type: ignore

    def test_comparison_operators(self):
        assert Capacity(10) < Capacity(20)
        assert Capacity(10) <= Capacity(10)
        assert Capacity(20) > Capacity(10)
        assert Capacity(20) >= Capacity(20)
        assert Capacity(10) == 10
        assert Capacity(10) != 20

    def test_arithmetic(self):
        assert Capacity(50) - Capacity(30) == 20
        assert 100 - Capacity(30) == 70


# =============================================================================
# CheckInStatus
# =============================================================================

class TestCheckInStatus:
    def test_valid_statuses(self):
        for s in ("not_checked_in", "checked_in", "NotCheckedIn", "CheckedIn"):
            assert str(CheckInStatus(s)) == s

    def test_invalid_status(self):
        with pytest.raises(ValueError):
            CheckInStatus("unknown")

    def test_equality_with_string(self):
        assert CheckInStatus("CheckedIn") == "CheckedIn"
        assert CheckInStatus("CheckedIn") != "NotCheckedIn"


# =============================================================================
# City
# =============================================================================

class TestCity:
    def test_valid(self):
        assert str(City("Brisbane")) == "Brisbane"

    def test_min_length(self):
        City("X")
        with pytest.raises(ValueError, match="1 to 80"):
            City("")

    def test_max_length(self):
        City("A" * 80)
        with pytest.raises(ValueError, match="1 to 80"):
            City("A" * 81)

    def test_invalid_characters(self):
        with pytest.raises(ValueError, match="English letters"):
            City("123City")

    def test_valid_with_special_chars(self):
        City("St. John's")
        City("New-York City")


# =============================================================================
# ContactNumber
# =============================================================================

class TestContactNumber:
    def test_valid(self):
        assert str(ContactNumber("0412345678")) == "0412345678"

    def test_valid_with_plus(self):
        assert str(ContactNumber("+61412345678")) == "+61412345678"

    def test_valid_with_spaces_hyphens(self):
        ContactNumber("0412 345 678")
        ContactNumber("0412-345-678")

    def test_min_length(self):
        ContactNumber("1")
        with pytest.raises(ValueError, match="1 to 20"):
            ContactNumber("")

    def test_max_length(self):
        ContactNumber("1" * 20)
        with pytest.raises(ValueError, match="1 to 20"):
            ContactNumber("1" * 21)

    def test_consecutive_spaces(self):
        with pytest.raises(ValueError, match="consecutive spaces"):
            ContactNumber("0412  345")

    def test_invalid_characters(self):
        with pytest.raises(ValueError, match="digits, spaces, hyphens"):
            ContactNumber("abc")


# =============================================================================
# DateTime
# =============================================================================

class TestDateTimeValue:
    def test_valid_datetime(self):
        dt = datetime(2026, 7, 1, 12, 0)
        d = DateTime(dt)
        assert d.value == dt

    def test_type_error(self):
        with pytest.raises(TypeError, match="datetime object"):
            DateTime("2026-07-01")  # type: ignore

    def test_string_isoformat(self):
        dt = datetime(2026, 7, 1, 12, 0, 0)
        d = DateTime(dt)
        assert "2026-07-01" in str(d)


# =============================================================================
# Email
# =============================================================================

class TestEmail:
    def test_valid(self):
        assert str(Email("test@example.com")) == "test@example.com"

    def test_min_length(self):
        Email("a@b.c")
        with pytest.raises(ValueError, match="3 to 120"):
            Email("ab")

    def test_max_length(self):
        user = "a" * 100
        domain = "b" * 15
        Email(f"{user}@{domain}.c")
        with pytest.raises(ValueError, match="3 to 120"):
            Email("a" * 121)

    def test_invalid_formats(self):
        invalid = ["notanemail", "@no-local.com", "no-domain@", "no at@sign.com"]
        for e in invalid:
            with pytest.raises(ValueError, match="format is invalid"):
                Email(e)

    def test_valid_edge_formats(self):
        Email("user+tag@example.com")
        Email("user.name@sub.example.co.uk")


# =============================================================================
# EventStatus
# =============================================================================

class TestEventStatus:
    def test_valid_statuses(self):
        for s in ("draft", "pending", "approved", "rejected", "published",
                    "cancelled", "finished", "Open", "Cancelled", "Sold Out", "Inactive"):
            assert str(EventStatus(s)) == s

    def test_invalid_status(self):
        with pytest.raises(ValueError):
            EventStatus("invalid")

    def test_equality_with_string(self):
        assert EventStatus("Open") == "Open"
        assert EventStatus("Open") != "Cancelled"


# =============================================================================
# EventTitle
# =============================================================================

class TestEventTitle:
    def test_valid(self):
        assert str(EventTitle("Jazz Night")) == "Jazz Night"

    def test_min_length(self):
        EventTitle("X")
        with pytest.raises(ValueError, match="1 to 100"):
            EventTitle("")

    def test_max_length(self):
        EventTitle("A" * 100)
        with pytest.raises(ValueError, match="1 to 100"):
            EventTitle("A" * 101)

    def test_leading_trailing_spaces(self):
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            EventTitle(" Title")


# =============================================================================
# Money
# =============================================================================

class TestMoney:
    def test_valid(self):
        m = Money(Decimal("19.99"))
        assert str(m) == "19.99"
        assert m.value == Decimal("19.99")

    def test_zero(self):
        assert str(Money(Decimal("0.00"))) == "0.00"

    def test_negative(self):
        with pytest.raises(ValueError, match="greater than or equal to 0"):
            Money(Decimal("-1.00"))

    def test_too_many_decimals(self):
        with pytest.raises(ValueError, match="2 decimal places"):
            Money(Decimal("1.999"))

    def test_type_error(self):
        with pytest.raises(TypeError):
            Money(10)  # type: ignore
        with pytest.raises(TypeError):
            Money("10.00")  # type: ignore


# =============================================================================
# MusicGenre
# =============================================================================

class TestMusicGenre:
    def test_valid(self):
        assert str(MusicGenre("Jazz")) == "Jazz"

    def test_min_length(self):
        MusicGenre("X")
        with pytest.raises(ValueError, match="1 to 80"):
            MusicGenre("")

    def test_max_length(self):
        MusicGenre("A" * 80)
        with pytest.raises(ValueError, match="1 to 80"):
            MusicGenre("A" * 81)

    def test_invalid_characters(self):
        with pytest.raises(ValueError, match="English letters"):
            MusicGenre("123")

    def test_with_hyphen(self):
        assert str(MusicGenre("Campus-Festival")) == "Campus-Festival"

    def test_equality(self):
        assert MusicGenre("Rock") == "Rock"
        assert MusicGenre("Jazz") != "Rock"


# =============================================================================
# Name
# =============================================================================

class TestName:
    def test_valid(self):
        assert str(Name("John")) == "John"

    def test_empty(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Name("")

    def test_max_length(self):
        Name("A" * 30)
        with pytest.raises(ValueError, match="longer than 30"):
            Name("A" * 31)

    def test_invalid_characters(self):
        for invalid in ["John123", "John_Doe", "John Doe", "Jöhn"]:
            with pytest.raises(ValueError, match="English letters"):
                Name(invalid)


# =============================================================================
# Nickname
# =============================================================================

class TestNickname:
    def test_valid(self):
        assert str(Nickname("user_123")) == "user_123"

    def test_empty(self):
        with pytest.raises(ValueError, match="1 to 50"):
            Nickname("")

    def test_max_length(self):
        Nickname("A" * 50)
        with pytest.raises(ValueError, match="1 to 50"):
            Nickname("A" * 51)

    def test_invalid_characters(self):
        for invalid in ["user name", "user@name", "user-name"]:
            with pytest.raises(ValueError, match="letters, numbers, and underscores"):
                Nickname(invalid)


# =============================================================================
# OrganizationName
# =============================================================================

class TestOrganizationName:
    def test_valid(self):
        assert str(OrganizationName("SoundWave Inc")) == "SoundWave Inc"

    def test_min_length(self):
        OrganizationName("X")
        with pytest.raises(ValueError, match="1 to 120"):
            OrganizationName("")

    def test_max_length(self):
        OrganizationName("A" * 120)
        with pytest.raises(ValueError, match="1 to 120"):
            OrganizationName("A" * 121)

    def test_leading_trailing_spaces(self):
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            OrganizationName(" Org")

    def test_repeated_spaces(self):
        with pytest.raises(ValueError, match="repeated spaces"):
            OrganizationName("Org  Name")


# =============================================================================
# PasswordHash
# =============================================================================

class TestPasswordHash:
    def test_valid(self):
        assert str(PasswordHash("hashed_value_123")) == "hashed_value_123"

    def test_empty(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            PasswordHash("")

    def test_max_length(self):
        PasswordHash("A" * 255)
        with pytest.raises(ValueError, match="longer than 255"):
            PasswordHash("A" * 256)

    def test_contains_spaces(self):
        with pytest.raises(ValueError, match="cannot contain spaces"):
            PasswordHash("hash with space")


# =============================================================================
# PaymentMethod
# =============================================================================

class TestPaymentMethod:
    def test_valid_methods(self):
        for m in ("card", "paypal", "bank_transfer", "free"):
            assert str(PaymentMethod(m)) == m

    def test_invalid(self):
        with pytest.raises(ValueError):
            PaymentMethod("bitcoin")


# =============================================================================
# PaymentStatus
# =============================================================================

class TestPaymentStatus:
    def test_valid_statuses(self):
        for s in ("pending", "paid", "refunded", "failed",
                    "Pending", "Paid", "Refunded", "Failed"):
            assert str(PaymentStatus(s)) == s

    def test_invalid(self):
        with pytest.raises(ValueError):
            PaymentStatus("unknown")

    def test_equality(self):
        assert PaymentStatus("Paid") == "Paid"
        assert PaymentStatus("Paid") != "Refunded"


# =============================================================================
# QRCode
# =============================================================================

class TestQRCode:
    def test_valid(self):
        q = QRCode("abc123-def456")
        assert str(q) == "abc123-def456"

    def test_min_length(self):
        QRCode("x")
        with pytest.raises(ValueError, match="1 to 255"):
            QRCode("")

    def test_max_length(self):
        QRCode("A" * 255)
        with pytest.raises(ValueError, match="1 to 255"):
            QRCode("A" * 256)

    def test_contains_spaces(self):
        with pytest.raises(ValueError, match="cannot contain spaces"):
            QRCode("abc 123")

    def test_non_ascii(self):
        with pytest.raises(ValueError, match="ASCII characters only"):
            QRCode("café")


# =============================================================================
# RegistrationStatus
# =============================================================================

class TestRegistrationStatus:
    def test_valid_statuses(self):
        for s in ("pending", "confirmed", "cancelled", "Pending", "Confirmed", "Cancelled"):
            assert str(RegistrationStatus(s)) == s

    def test_invalid(self):
        with pytest.raises(ValueError):
            RegistrationStatus("active")

    def test_equality(self):
        assert RegistrationStatus("Confirmed") == "Confirmed"
        assert RegistrationStatus("Confirmed") != "Cancelled"


# =============================================================================
# Room
# =============================================================================

class TestRoom:
    def test_valid(self):
        assert str(Room("Main Hall")) == "Main Hall"

    def test_min_length(self):
        Room("A")
        with pytest.raises(ValueError, match="1 to 80"):
            Room("")

    def test_max_length(self):
        Room("A" * 80)
        with pytest.raises(ValueError, match="1 to 80"):
            Room("A" * 81)

    def test_leading_trailing_spaces(self):
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            Room(" Room")


# =============================================================================
# Text100
# =============================================================================

class TestText100:
    def test_valid(self):
        assert str(Text100("Short bio")) == "Short bio"

    def test_empty_allowed(self):
        Text100("")

    def test_max_length(self):
        Text100("A" * 100)
        with pytest.raises(ValueError, match="longer than 100"):
            Text100("A" * 101)

    def test_none_not_allowed(self):
        with pytest.raises(ValueError, match="cannot be None"):
            Text100(None)  # type: ignore


# =============================================================================
# Text200
# =============================================================================

class TestText200:
    def test_valid(self):
        assert str(Text200("Event description")) == "Event description"

    def test_empty_not_allowed(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Text200("")

    def test_max_length(self):
        Text200("A" * 200)
        with pytest.raises(ValueError, match="longer than 200"):
            Text200("A" * 201)


# =============================================================================
# Text500
# =============================================================================

class TestText500:
    def test_valid(self):
        assert str(Text500("Comment")) == "Comment"

    def test_empty_not_allowed(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Text500("")

    def test_max_length(self):
        Text500("A" * 500)
        with pytest.raises(ValueError, match="longer than 500"):
            Text500("A" * 501)

    def test_leading_trailing_spaces(self):
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            Text500(" text")


# =============================================================================
# TicketStatus
# =============================================================================

class TestTicketStatus:
    def test_valid_statuses(self):
        for s in ("valid", "cancelled", "used", "Valid", "Cancelled", "Used"):
            assert str(TicketStatus(s)) == s

    def test_invalid(self):
        with pytest.raises(ValueError):
            TicketStatus("expired")

    def test_equality(self):
        assert TicketStatus("Valid") == "Valid"
        assert TicketStatus("Valid") != "Cancelled"


# =============================================================================
# TicketType
# =============================================================================

class TestTicketType:
    def test_valid_types(self):
        for t in ("free", "standard", "vip"):
            assert str(TicketType(t)) == t

    def test_invalid(self):
        with pytest.raises(ValueError):
            TicketType("premium")


# =============================================================================
# VenueName
# =============================================================================

class TestVenueName:
    def test_valid(self):
        assert str(VenueName("Opera House")) == "Opera House"

    def test_min_length(self):
        VenueName("A")
        with pytest.raises(ValueError, match="1 to 120"):
            VenueName("")

    def test_max_length(self):
        VenueName("A" * 120)
        with pytest.raises(ValueError, match="1 to 120"):
            VenueName("A" * 121)

    def test_leading_trailing_spaces(self):
        with pytest.raises(ValueError, match="cannot start or end with spaces"):
            VenueName(" Name")


# =============================================================================
# ID Value Objects
# =============================================================================

class TestIdValueObjects:
    """All ID value objects follow the same pattern: positive integer."""

    ID_CLASSES = [UserId, AdminId, ArtistId, EventId, OrganizerId,
                  ParticipantId, PaymentId, RegistrationId, TicketId, VenueId]

    @pytest.mark.parametrize("cls", ID_CLASSES)
    def test_valid_id(self, cls):
        assert int(cls(42)) == 42

    @pytest.mark.parametrize("cls", ID_CLASSES)
    def test_id_lower_boundary(self, cls):
        with pytest.raises(ValueError, match="greater than 0"):
            cls(0)

    @pytest.mark.parametrize("cls", ID_CLASSES)
    def test_id_negative(self, cls):
        with pytest.raises(ValueError, match="greater than 0"):
            cls(-1)

    @pytest.mark.parametrize("cls", ID_CLASSES)
    def test_id_type_error(self, cls):
        with pytest.raises(TypeError):
            cls("42")  # type: ignore
        with pytest.raises(TypeError):
            cls(42.0)  # type: ignore
