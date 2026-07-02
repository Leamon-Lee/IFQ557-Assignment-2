# SoundWave Events Frontend API Contract

This document describes the backend endpoints expected by the SoundWave Events frontend prototype.

The current frontend can be demonstrated without a live backend. Buttons that depend on backend work use `data-api-method` and `data-api-endpoint` attributes to show the intended integration point.

## Base response format

Successful responses should return JSON:

```json
{
  "success": true,
  "message": "Operation completed.",
  "data": {}
}
```

Error responses should return JSON:

```json
{
  "success": false,
  "message": "Readable error message.",
  "errors": {}
}
```

## Authentication

### Login

`POST /api/auth/login`

Used by the login form.

Request body:

```json
{
  "email": "you@example.com",
  "password": "password",
  "login_role": "participant"
}
```

`login_role` can be:

- `participant`
- `organizer`

Expected response:

```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "user_id": 1,
    "nickname": "bacon",
    "role": "participant",
    "redirect_url": "/participant/registrations"
  }
}
```

Backend requirement:

- Verify email and password.
- Verify that the selected `login_role` matches the account role.
- Return role-specific redirect URL.

### Register

`POST /api/auth/register`

Used by the create account form.

Common request body:

```json
{
  "account_type": "participant",
  "first_name": "Alex",
  "second_name": "Chen",
  "nickname": "alexchen",
  "contact_number": "+86 138 0000 0000",
  "email": "you@example.com",
  "street_address": "123 Main Street",
  "password": "password"
}
```

Organizer request body:

```json
{
  "account_type": "organizer",
  "first_name": "Alex",
  "second_name": "Chen",
  "nickname": "alexchen",
  "contact_number": "+86 138 0000 0000",
  "email": "you@example.com",
  "street_address": "123 Main Street",
  "password": "password",
  "organization_name": "SoundWave Club",
  "bio": "Campus music event organizer."
}
```

Expected response:

```json
{
  "success": true,
  "message": "Account created.",
  "data": {
    "user_id": 8,
    "role": "organizer",
    "redirect_url": "/auth/login"
  }
}
```

Backend requirement:

- Create `Participant` when `account_type` is `participant`.
- Create `Organizer` when `account_type` is `organizer`.
- Require `organization_name` for organizer accounts.

## Events

### List events

`GET /api/events`

Query parameters:

- `genre`
- `search`
- `date`

Expected response:

```json
{
  "success": true,
  "data": {
    "events": [
      {
        "event_id": 1,
        "event_title": "Riverside Jazz Night",
        "music_genre": "Jazz",
        "venue_name": "Blue Hall",
        "start_time": "2026-07-12T19:00:00",
        "event_status": "Open",
        "remaining_tickets": 38
      }
    ]
  }
}
```

### Event detail

`GET /api/events/{event_id}`

Expected response includes event details, venue, artists, ticket availability, comments and announcements.

### Create event

`POST /api/events`

Organizer-only endpoint used by the create event page.

Request body:

```json
{
  "event_title": "Campus Music Festival",
  "description": "Student bands and outdoor market atmosphere.",
  "music_genre": "Campus Festival",
  "venue_id": 2,
  "start_time": "2026-07-14T18:00:00",
  "end_time": "2026-07-14T22:00:00",
  "capacity": 300,
  "age_restriction": 0
}
```

### Update event

`PUT /api/events/{event_id}`

Organizer-only endpoint used by the edit event page.

### Cancel event

`POST /api/events/{event_id}/cancel`

Organizer-only endpoint used by event management.

## Bookings and tickets

### Create booking

`POST /api/events/{event_id}/book`

Participant-only endpoint used by the event detail booking panel.

Request body:

```json
{
  "quantity": 1,
  "ticket_type": "standard",
  "price": "25.00",
  "payment_method": "card"
}
```

Expected response:

```json
{
  "success": true,
  "message": "Booking confirmed.",
  "data": {
    "order_ids": ["SW-2026-0003"]
  }
}
```

### List my bookings

`GET /api/me/bookings`

Used by the booking history page.

### Cancel booking

`POST /api/bookings/{registration_id}/cancel`

Used by the `Cancel booking` buttons.

Frontend attributes:

```html
data-api-method="POST"
data-api-endpoint="/api/bookings/{registration_id}/cancel"
```

Expected response:

```json
{
  "success": true,
  "message": "Booking cancelled.",
  "data": {
    "registration_status": "Cancelled",
    "ticket_status": "Cancelled",
    "payment_status": "Refunded"
  }
}
```

### View ticket

`GET /api/tickets/{ticket_id}`

Used by the ticket detail page.

## Organizer tools

### List participants for an event

`GET /api/organizer/events/{event_id}/participants`

Used by the organizer participant list page.

### Mark participant checked in

`POST /api/organizer/registrations/{registration_id}/check-in`

Used by the `Mark checked in` button.

Frontend attributes:

```html
data-api-method="POST"
data-api-endpoint="/api/organizer/registrations/{registration_id}/check-in"
```

Expected response:

```json
{
  "success": true,
  "message": "Participant checked in.",
  "data": {
    "check_in_status": "CheckedIn",
    "ticket_status": "Used"
  }
}
```

### Post announcement

`POST /api/organizer/events/{event_id}/announcements`

Used by the organizer announcement form.

Request body:

```json
{
  "content": "Please arrive 20 minutes before the show starts."
}
```

Validation:

- `content` is required.
- Maximum length is 500 characters.

## Comments

### Post comment

`POST /api/events/{event_id}/comments`

Used by the event detail comment form.

Request body:

```json
{
  "content": "Really excited for this event!"
}
```

## Role-based frontend behavior

The frontend expects the backend to return a user role after login:

- `participant`: show booking history and ticket actions.
- `organizer`: show create event, organizer dashboard, participant list and check-in actions.
- `admin`: show admin dashboard and event review tools.

The frontend registration form submits `account_type` so the backend can create the correct user class.
