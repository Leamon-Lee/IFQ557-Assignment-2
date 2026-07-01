from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.comment_forms import CommentForm
from app.services.comment_service import CommentService
from app.services.event_service import EventService


event_bp = Blueprint("events", __name__)


@event_bp.route("/")
def index():
    service = EventService()
    events = service.listEvents()

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

    return render_template(
        "index.html",
        featured_events=featured,
        all_events=event_data,
    )


@event_bp.route("/events")
def list_events():
    service = EventService()
    events = service.listEvents()
    return render_template("events/list.html", events=events)


@event_bp.route("/events/create", methods=["GET", "POST"])
def create_event():
    return render_template("events/create.html")


@event_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id: int):
    return render_template("events/edit.html")


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

    remaining = service.getRemainingTickets(event_id)
    confirmed = service.getConfirmedCount(event_id)
    fill_pct = round(confirmed / event.capacity * 100, 1) if event.capacity > 0 else 0
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
    )