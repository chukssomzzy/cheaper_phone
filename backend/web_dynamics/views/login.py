#!/usr/bin/env -s venv/bin/python3
"""login view """

from flask_login import login_user
from models import storage
from models.users import User
from web_dynamics.utils.forms.login_customer import LoginUserForm

from web_dynamics.views import web_dynamics
from flask import jsonify, make_response, request


@web_dynamics.route("/login", methods=["POST", "GET"], strict_slashes=False)
def login():
    """login user"""
    form = LoginUserForm(formdata=request.form)
    if form.validate():
        user = None
        if form.email.data:
            user = storage.session.query(User).filter_by(
                email=form.email.data).one_or_none()
        elif form.username.data:
            user = storage.session.query(User).filter_by(
                username=form.username.data).one_or_none()
        if user and bool(user.check_password(form.password.data)):
            login_user(user)
            return make_response(jsonify({"login": "success"}), 200)
    return make_response(
        jsonify({"error": "incorrect username or Password"}), 401)
