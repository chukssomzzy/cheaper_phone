#!/usr/bin/env -S venv/bin/python3
"""Login user route"""

from models import storage
from models.users import User
from wtforms import (Form, PasswordField, StringField, ValidationError,
                     validators)


def is_user_pass(form, field):
    """confirm the  input password"""
    if form.username.data:
        user = storage.session.query(User).filter_by(
            username=form.username.data).one_or_none()
        if user and bool(user.check_password(field.data)):
            return None
    if form.email.data:
        user = storage.session.query(User).filter_by(
            email=form.email.data).one_or_none()
        if user and bool(user.check_password(field.data)):
            return None
    raise ValidationError("Incorrect Username or Password")


def email_or_username(form, field):
    """limit form to email or password"""
    if form.email.data and form.username.data:
        raise ValidationError("Form must contain either username or email")


class LoginUserForm(Form):
    """Login form"""
    email = StringField(
        "Email Address", [email_or_username])
    password = PasswordField(
        "Password", [validators.InputRequired(message="password required"),
                     is_user_pass])
    username = StringField("Email Address", [email_or_username])
