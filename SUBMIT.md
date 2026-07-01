# Submission Notes - SoundWave Events

## Project Name

SoundWave Events

## Repository Branches

This submission is pushed to both:

- `leamon`
- `main`

## Environment

Python version:

```text
Python 3.14.6
```

Recommended environment:

```powershell
conda activate musicevent
```

Install dependencies:

```powershell
pip install -r requirement.txt
```

Initialize the SQLite database:

```powershell
python init_db.py
```

Run the Flask application:

```powershell
python run.py
```

Open the site:

```text
http://127.0.0.1:5000
```

## Main Work Completed

The project has been built as a Flask MVC web application using:

- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-WTF
- Flask-Login
- Flask-Bcrypt
- Bootstrap-Flask
- Jinja2 templates

The current project contains:

- Flask application factory
- SQLAlchemy models
- MVC-style project folders
- Blueprint routes
- Service layer placeholders
- Form classes
- Jinja2 templates
- Static frontend assets
- SQLite initialization script
- UML image and README documentation
- Domain value objects with validation rules

## UML Implementation Summary

The UML classes represented in the project are:

- `User`
- `Participant`
- `Organizer`
- `Admin`
- `MusicEvent`
- `Venue`
- `Artist`
- `Registration`
- `Ticket`
- `Payment`

The key UML relationships have been reflected in the SQLAlchemy models:

- `Participant` inherits from `User`
- `Organizer` inherits from `User`
- `Admin` is independent and does not inherit from `User`
- One organizer can create many music events
- One music event belongs to one organizer
- One venue can host many music events
- One music event belongs to one venue
- Music events and artists use a many-to-many association table named `event_artist`
- One participant can have many registrations
- One music event can have many registrations
- One registration can have one ticket
- One registration can have zero or one payment

## Value Object Design

The project uses strict value objects under:

```text
app/domain/value_objects/
```

Each value object is stored in its own file. The models use these value objects instead of passing raw strings or integers directly in important places.

Examples:

```python
Nickname("Leamon")
Email("leamon@example.com")
Name("Paul")
Capacity(100)
Money(Decimal("10.50"))
EventStatus("draft")
TicketType("standard")
```

Invalid data raises an error immediately.

Examples of rejected values:

- `UserId(0)`
- `Name("Leamon Lee")`
- `Email("bad")`
- `Capacity(-1)`
- `Age(101)`
- `Money(Decimal("1.999"))`
- `QRCode("BAD QR")`

## Completed Value Objects

The following value objects are implemented:

- `Address`
- `AdminId`
- `Age`
- `AgeRestriction`
- `ArtistId`
- `ArtistType`
- `Capacity`
- `CheckInStatus`
- `City`
- `DateTime`
- `Email`
- `EventId`
- `EventStatus`
- `EventTitle`
- `Money`
- `MusicGenre`
- `Name`
- `Nickname`
- `OrganizerId`
- `OrganizationName`
- `ParticipantId`
- `PasswordHash`
- `PaymentId`
- `PaymentMethod`
- `PaymentStatus`
- `QRCode`
- `RegistrationId`
- `RegistrationStatus`
- `Room`
- `Text100`
- `Text200`
- `TicketId`
- `TicketStatus`
- `TicketType`
- `UserId`
- `VenueId`
- `VenueName`

## Important Validation Rules

Some examples of validation rules:

- `Name`: English letters only, no spaces, maximum 30 characters
- `Nickname`: 1 to 50 characters, English letters, numbers, and underscores only
- `Email`: 3 to 120 characters and valid basic email format
- `Capacity`: integer, greater than 0, maximum 100000
- `Age`: integer, between 0 and 100
- `Money`: `Decimal`, greater than or equal to 0, maximum 2 decimal places
- `QRCode`: 1 to 255 characters, ASCII only, no spaces
- `EventStatus`: must be one of `draft`, `pending`, `approved`, `rejected`, `published`, `cancelled`, `finished`
- `TicketType`: must be one of `free`, `standard`, `vip`
- `PaymentStatus`: must be one of `pending`, `paid`, `refunded`, `failed`

## Frontend Integration

The frontend prototype has been merged into the Flask template structure.

Frontend files are now located under:

```text
app/templates/
app/static/
```

The pages have been connected to Flask routes using `render_template`.

Tested pages include:

- `/`
- `/auth/login`
- `/events/1`
- `/events/create`

## Verification

The following checks were run successfully:

```powershell
conda run -n musicevent python -m compileall app config.py init_db.py run.py
```

Flask smoke tests returned HTTP 200 for:

```text
/
/auth/login
/events/1
/events/create
```

Value object validation was also tested with both valid and invalid examples.

## Current Development Status

The project structure, model layer, value objects, frontend templates, and documentation are prepared.

Some business logic is still incomplete by design. Several methods remain as placeholders or simple stubs because the project was initially requested as a UML/MVC scaffold. Future work should complete:

- Authentication flow
- Signup form integration
- Event CRUD logic
- Registration and ticket generation
- Payment workflow
- Admin approval and rejection workflow
