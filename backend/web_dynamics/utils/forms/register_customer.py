import re

from flask_wtf import FlaskForm
from flask_wtf.csrf import ValidationError
from wtforms import StringField, validators
from wtforms.fields import PasswordField


def strong_password(form, field):
    """Test if a password is strong"""
    p = re.compile(
        "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\\-=\\[\\]{};':\",\
.<>?])(?=.{8,})")
    if not p.match(field.data):
        raise ValidationError("password must be strong")


class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField(
        "Username", [validators.InputRequired(message="username required")])
    email = StringField(
        "Email Address", [validators.length(min=6, max=60,
                                            message="Too short for email"),
                          validators.Email(message="Wrong email password")])
    password = PasswordField("Password", [validators.InputRequired(
        message="password is required"), strong_password])
