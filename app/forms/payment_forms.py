from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PaymentForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField("Payment Method", choices=[("card", "Card"), ("paypal", "PayPal"), ("bank_transfer", "Bank Transfer"), ("free", "Free")])
    submit = SubmitField("Pay")
