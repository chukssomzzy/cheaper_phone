#!/usr/bin/env -S venv/bin/python3
"""Contains register user form"""

import re

from flask_wtf import FlaskForm
from flask_wtf.csrf import ValidationError
from models import storage
from models.users import User
from wtforms import StringField, validators
from wtforms.fields import PasswordField


def strong_password(form, field):
    """Test if a password is strong"""
    p = re.compile(
        "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\\-=\\[\\]{};':\",\
.<>?])(?=.{8,})")
    if not p.match(field.data):
        raise ValidationError("password must be strong")


class IsUnique():
    """checks if a field is unique"""

    def __init__(self, cls=User, attr="username", message=None):
        self.attr = attr
        self.cls = cls
        if not message:
            message = f'{cls.__name__} with {attr} already exist'
        self.message = message

    def __call__(self, form, field):
        """Test if a attr exit in a model"""
        if storage.session.query(self.cls).filter(
                getattr(self.cls, self.attr) == field.data).one_or_none():
            raise ValidationError(self.message)


isunique = IsUnique


class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField(
        "Username", [validators.InputRequired(message="username required"),
                     isunique(message="username taken")])
    email = StringField(
        "Email Address", [validators.length(min=6, max=60,
                                            message="Too short for email"),
                          validators.Email(), isunique(attr="email")])
    password = PasswordField("Password", [validators.InputRequired(
        message="password is required"), strong_password])
