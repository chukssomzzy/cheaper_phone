#!/usr/bin/env -S venv/bin/python3
"""Login user route"""

from models import storage
from models.users import User
from wtforms import (Form, PasswordField, StringField, ValidationError,
                     validators)


def is_user_pass(form, field):
    """confirm the  input password"""
    if form.email.data:
        user = storage.session.query(User).filter_by(
            email=form.email.data).one_or_none()
        if not user:
            raise ValidationError("Incorrect Username or Password")
        elif not bool(user.check_password(field.data)):
            raise ValidationError("Incorrect Username or Password")


class LoginUserForm(Form):
    """Login form"""
    email = StringField(
        "Email Address", [validators.InputRequired(message="email required")])
    password = PasswordField(
        "Password", [validators.InputRequired(message="password required"),
                     is_user_pass])
