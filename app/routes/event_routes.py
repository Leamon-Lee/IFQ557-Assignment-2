from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms.comment_forms import CommentForm
from app.forms.event_forms import EventForm
from app.domain.value_objects import AgeRestriction, Capacity, DateTime, EventTitle, MusicGenre, Text200, EventStatus
from app.models.announcement import Announcement
from app.models.music_event import MusicEvent
from app.models.organizer import Organizer
from app.models.venue import Venue
from app.services.comment_service import CommentService
from app.services.event_service import EventService


event_bp = Blueprint("events", __name__)


@event_bp.route("/")
@event_bp.route("/loading")
def loading():
    return render_template("loading.html")


def _get_organizer():
    return Organizer.query.filter_by(organizer_id=current_user.user_id).first()


def _get_venue_choices():
    venues = Venue.query.order_by(Venue.venue_name).all()
    return [(v.venue_id, f"{v.venue_name} ({v.city})") for v in venues]


@event_bp.route("/index")
def index():
    genre = request.args.get("genre")
    search = request.args.get("search")
    date_filter = request.args.get("date")

    service = EventService()
    events = service.listEvents(
        genre=genre if genre else None,
        search=search if search else None,
        date_filter=date_filter if date_filter else None,
    )

    event_data = []
    for e in events:
        event_data.append({
            "event": e,
            "remaining": service.getRemainingTickets(e.event_id),
            "confirmed": service.getConfirmedCount(e.event_id),
            "venue_name": e.venue.venue_name if e.venue else "TBA",
            "artist_names": ", ".join(
                f"{a.first_name} {a.second_name}".strip() for a in e.artists
            ) if e.artists else "TBA",
        })

    featured = [d for d in event_data if d["event"].event_status == "Open"][:3]

    genres = ["Jazz", "Rock", "Campus Festival", "Acoustic", "Concert"]

    return render_template(
        "index.html",
        featured_events=featured,
        all_events=event_data,
        genres=genres,
        current_genre=genre,
        current_search=search,
        current_date=date_filter,
    )


@event_bp.route("/events")
def list_events():
    genre = request.args.get("genre")
    service = EventService()
    events = service.listEvents(genre if genre else None)

    event_data = []
    for e in events:
        event_data.append({
            "event": e,
            "remaining": service.getRemainingTickets(e.event_id),
            "venue_name": e.venue.venue_name if e.venue else "TBA",
            "artist_names": ", ".join(
                f"{a.first_name} {a.second_name}".strip() for a in e.artists
            ) if e.artists else "TBA",
        })

    genres = ["Jazz", "Rock", "Campus Festival", "Acoustic", "Concert"]

    return render_template(
        "events/list.html",
        events=event_data,
        genres=genres,
        current_genre=genre,
    )


@event_bp.route("/events/create", methods=["GET", "POST"])
@login_required
def create_event():
    org = _get_organizer()
    if org is None:
        flash("You need an organizer account to create events.", "danger")
        return redirect(url_for("events.index"))

    form = EventForm()
    form.venue_id.choices = _get_venue_choices()

    if form.validate_on_submit():
        event = MusicEvent(
            event_title=EventTitle(form.event_title.data),
            description=Text200(form.description.data),
            start_time=DateTime(form.start_time.data),
            end_time=DateTime(form.end_time.data),
            capacity=Capacity(form.capacity.data),
            age_restriction=AgeRestriction(form.age_restriction.data),
            music_genre=MusicGenre(form.music_genre.data),
            organizer_id=org.organizer_id,
            venue_id=form.venue_id.data,
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for("events.event_detail", event_id=event.event_id))

    return render_template("events/create.html", form=form)


@event_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id: int):
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        abort(404)

    if event.organizer_id != current_user.user_id:
        flash("You can only edit your own events.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    form = EventForm(obj=event)
    form.venue_id.choices = _get_venue_choices()

    if form.validate_on_submit():
        event.event_title = EventTitle(form.event_title.data)
        event.description = Text200(form.description.data)
        event.start_time = DateTime(form.start_time.data)
        event.end_time = DateTime(form.end_time.data)
        event.capacity = Capacity(form.capacity.data)
        event.age_restriction = AgeRestriction(form.age_restriction.data)
        event.music_genre = MusicGenre(form.music_genre.data)
        event.venue_id = form.venue_id.data
        event.event_status = EventStatus(form.event_status.data)
        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for("events.event_detail", event_id=event_id))

    return render_template("events/edit.html", form=form, event=event)


@event_bp.route("/events/<int:event_id>/cancel", methods=["POST"])
@login_required
def cancel_event(event_id: int):
    event = db.session.get(MusicEvent, event_id)
    if event is None:
        abort(404)

    if event.organizer_id != current_user.user_id:
        flash("You can only cancel your own events.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    if event.event_status == "Cancelled":
        flash("This event is already cancelled.", "info")
    else:
        event.cancel()
        flash("Event has been cancelled.", "info")

    return redirect(url_for("events.event_detail", event_id=event_id))


@event_bp.route("/events/<int:event_id>", methods=["GET", "POST"])
def event_detail(event_id: int):
    service = EventService()
    event = service.getEvent(event_id)
    if event is None:
        abort(404)

    comment_service = CommentService()
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to post a comment.", "warning")
            return redirect(url_for("auth.login"))
        comment_service.addComment(
            user_id=current_user.user_id,
            event_id=event_id,
            content=comment_form.content.data,
        )
        flash("Comment posted.", "success")
        return redirect(url_for("events.event_detail", event_id=event_id))

    comments = comment_service.getCommentsByEvent(event_id)
    announcements = (
        Announcement.query
        .filter_by(event_id=event_id)
        .order_by(Announcement.created_at.desc())
        .all()
    )

    remaining = service.getRemainingTickets(event_id)
    confirmed = service.getConfirmedCount(event_id)
    fill_pct = round(confirmed / int(event.capacity) * 100, 1) if event.capacity > 0 else 0
    bar_style = f"width: {fill_pct}%"

    artist_names = ", ".join(
        f"{a.first_name} {a.second_name}".strip() for a in event.artists
    ) if event.artists else "TBA"

    return render_template(
        "events/detail.html",
        event=event,
        remaining=remaining,
        confirmed=confirmed,
        artist_names=artist_names,
        fill_pct=fill_pct,
        bar_style=bar_style,
        comments=comments,
        comment_form=comment_form,
        announcements=announcements,
    )
