#!/usr/bin/env -S venv/bin/python3
"""Login view """

from flask_login import login_user
from models import storage
from models.users import User

from web_dynamics.utils.forms.login_customer import LoginUserForm
from web_dynamics.views import web_dynamics
from flask import jsonify, make_response, request


@web_dynamics.route("/login", methods=["POST"], strict_slashes=False)
def login():
    """Login user"""
    form = LoginUserForm(formdata=request.form)

    if form.validate():
        user = storage.session.query(User).filter_by(
            username=form.username.data).one_or_none()
        if bool(user) and bool(user.check_password(form.password.data)):
            login_user(user)
    return make_response(
        jsonify({"error": "Incorrect Username Or Password"}), 400)
