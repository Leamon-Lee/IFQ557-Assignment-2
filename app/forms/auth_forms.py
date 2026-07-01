from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=1, max=80)])
    second_name = StringField("Surname", validators=[DataRequired(), Length(min=1, max=80)])
    contact_number = StringField("Contact Number", validators=[DataRequired(), Length(min=1, max=20)])
    street_address = StringField("Street Address", validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField("Create account")
