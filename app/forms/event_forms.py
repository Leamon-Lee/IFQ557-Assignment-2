from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class EventForm(FlaskForm):
    event_title = StringField("Event Title", validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=200)])
    start_time = DateTimeLocalField("Start Time", validators=[DataRequired()])
    end_time = DateTimeLocalField("End Time", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired(), NumberRange(min=1)])
    age_restriction = IntegerField("Age Restriction", validators=[DataRequired(), NumberRange(min=0, max=100)])
    music_genre = StringField("Music Genre", validators=[DataRequired()])
    submit = SubmitField("Save")
