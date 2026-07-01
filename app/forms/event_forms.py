from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

GENRE_CHOICES = [
    ("Jazz", "Jazz"),
    ("Rock", "Rock"),
    ("Campus Festival", "Campus Festival"),
    ("Acoustic", "Acoustic"),
    ("Concert", "Concert"),
]


class EventForm(FlaskForm):
    event_title = StringField("Event Title", validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=200)])
    music_genre = SelectField("Category", choices=GENRE_CHOICES, validators=[DataRequired()])
    start_time = DateTimeLocalField("Start Time", validators=[DataRequired()])
    end_time = DateTimeLocalField("End Time", validators=[DataRequired()])
    capacity = IntegerField("Total Tickets", validators=[DataRequired(), NumberRange(min=1)])
    age_restriction = IntegerField("Age Restriction", validators=[DataRequired(), NumberRange(min=0, max=100)])
    venue_id = SelectField("Venue", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save Event")
