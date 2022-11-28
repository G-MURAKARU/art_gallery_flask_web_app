from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from ..models import Customer


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Physical Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_name(self, name):
        customer = Customer.query.filter_by(customerName=name.data).first()
        if customer:
            raise ValidationError('This name has already been taken.')

    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('This email address has already been taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class PurchaseForm(FlaskForm):
#     card_number = IntegerField('Card Number', validators=[DataRequired(), Length(min=6, max=6)])
#     cvc = IntegerField('CVC', validators=[DataRequired(), Length(min=3, max=3)])
#     card_holder = StringField('Card Holder', validators=[DataRequired()])
#     submit = SubmitField('Purchase')
